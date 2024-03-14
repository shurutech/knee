from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager

config_dir = "playbooks/group_vars"


class Mysql:
    config_files = ["mysqlmainserver.yml"]
    configs = {}

    def __init__(self, replica_server_acceptance=False):
        self.file_manager = FileManager()
        if replica_server_acceptance:
            Mysql.config_files.append("mysqlreplicaservers.yml")
        for config_file in Mysql.config_files:
            Mysql.configs[config_file] = self.file_manager.read_from_file(
                config_dir, config_file
            )

    def parameter_configuration(self):
        Mysql.configs = load_configuration(Mysql.configs)
