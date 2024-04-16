from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook
from src.utils.constants.enum import Environment
from constants import VARIABLE_DIR_PATH


class Mysql:
    CONFIG_FILES = ["mysqlmainserver.yml"]
    REPLICA_CONFIG_FILES = ["mysqlmainserver.yml", "mysqlreplicaservers.yml"]

    def __init__(self, is_replica_required=False, environment=Environment.LOCAL.value):
        self.configs = {}
        self.is_replica_required = is_replica_required
        self.config_files = self.CONFIG_FILES if not is_replica_required else self.REPLICA_CONFIG_FILES
        self.file_manager = FileManager()
        self.environment = environment
        for config_file in self.config_files:
            self.configs[config_file] = self.file_manager.read_from_file(
                VARIABLE_DIR_PATH, config_file
            )

    def update_configuration(self):
        self.configs = load_configuration(self.configs)

    def apply_configuration(self):
        for config_file in self.config_files:
            self.file_manager.write_to_file(
                VARIABLE_DIR_PATH, config_file, self.configs[config_file]
            )
        if self.is_replica_required:
            run_playbook("mysql_replica_server.yml", self.environment)
        else:
            run_playbook("mysql_server.yml", self.environment)

