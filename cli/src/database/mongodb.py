from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook
from src.utils.constants.enum import Environment, MongodbFile
from constants import VARIABLE_DIR_PATH



class Mongodb:
    CONFIG_FILES = [MongodbFile.MONGODB_MAIN_SERVER.value]
    REPLICA_CONFIG_FILES = [MongodbFile.MONGODB_MAIN_SERVER.value, MongodbFile.MONGODB_REPLICA_SERVER.value]

    def __init__(self, is_replica_required=False, environment=Environment.LOCAL.value):
        self.configs = {}
        self.config_files = self.CONFIG_FILES if not is_replica_required else self.REPLICA_CONFIG_FILES
        self.environment = environment
        self.is_replica_required = is_replica_required
        self.file_manager = FileManager()
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
            run_playbook(MongodbFile.MONGODB_REPLICA_SERVER_PLAYBOOK.value, self.environment)
        else:    
            run_playbook(MongodbFile.MONGODB_SERVER_PLAYBOOK.value, self.environment)
