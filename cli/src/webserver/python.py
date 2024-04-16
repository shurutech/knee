from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook
from src.utils.constants.enum import Environment, PythonFile
from constants import VARIABLE_DIR_PATH


class Python:
    CONFIG_FILES = [PythonFile.PYTHON_WEBSERVERS.value]

    def __init__(self, environment=Environment.LOCAL.value):
        self.configs = {}
        self.environment = environment
        self.file_manager = FileManager()
        for config_file in self.CONFIG_FILES:
            self.configs[config_file] = self.file_manager.read_from_file(
                VARIABLE_DIR_PATH, config_file
            )

    def update_configuration(self):
        self.configs = load_configuration(self.configs)

    def apply_configuration(self):
        for config_file in self.CONFIG_FILES:
            self.file_manager.write_to_file(
                VARIABLE_DIR_PATH, config_file, self.configs[config_file]
            )
        run_playbook("webserver_base.yml", self.environment)
        run_playbook(PythonFile.PYTHON_SERVER_PLAYBOOK.value, self.environment)

