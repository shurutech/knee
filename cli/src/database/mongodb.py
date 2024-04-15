from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook

config_dir = "playbooks/group_vars"


class Mongodb:
    def __init__(self, is_replica_required=False, environment="local"):
        self.config_files = ["mongodbmainserver.yml"]
        self.configs = {}
        self.environment = environment
        self.is_replica_required = is_replica_required
        self.file_manager = FileManager()
        if is_replica_required:
            self.config_files.append("mongodbreplicaservers.yml")
        for config_file in self.config_files:
            self.configs[config_file] = self.file_manager.read_from_file(
                config_dir, config_file
            )

    def update_configuration(self):
        self.configs = load_configuration(self.configs)

    def apply_configuration(self):
        for config_file in self.config_files:
            self.file_manager.write_to_file(
                config_dir, config_file, self.configs[config_file]
            )
        if self.is_replica_required:
            run_playbook("mongodb_replica_server.yml", self.environment)
        else:    
            run_playbook("mongodb_server.yml", self.environment)
