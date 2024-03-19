from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook

config_dir = "playbooks/group_vars"


class Mysql:
    CONFIG_FILES = ["mysqlmainserver.yml"]
    REPLICA_CONFIG_FILES = ["mysqlmainserver.yml", "mysqlreplicaservers.yml"]

    def __init__(self, replica_server_acceptance=False, environment="local"):
        self.configs = {}
        self.config_files = self.CONFIG_FILES if not replica_server_acceptance else self.REPLICA_CONFIG_FILES
        self.file_manager = FileManager()
        self.environment = environment
        for config_file in self.CONFIG_FILES:
            self.configs[config_file] = self.file_manager.read_from_file(
                config_dir, config_file
            )

    def parameter_configuration(self):
        self.configs = load_configuration(self.configs)

    def write_configuration_and_run_playbook(self):
        for config_file in self.CONFIG_FILES:
            self.file_manager.write_to_file(
                config_dir, config_file, self.configs[config_file]
            )
        run_playbook("mysql_server.yml", self.environment)
