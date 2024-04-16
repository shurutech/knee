from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook
from src.utils.constants.enum import Environment, PostgresqlFile
from constants import VARIABLE_DIR_PATH


class Postgresql:
    config_files = [PostgresqlFile.POSTGRESQL_MAIN_SERVER.value]
    configs = {}

    def __init__(self, is_replica_required=False, environment=Environment.LOCAL.value):
        self.file_manager = FileManager()
        self.environment = environment
        self.is_replica_required = is_replica_required
        if is_replica_required:
            self.config_files.append(PostgresqlFile.POSTGRESQL_REPLICA_SERVER.value)
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
        run_playbook(PostgresqlFile.POSTGRESQL_SERVER_PLAYBOOK.value, self.environment)
        if self.is_replica_required:
            run_playbook(PostgresqlFile.POSTGRESQL_REPLICA_SERVER_PLAYBOOK.value, self.environment)

