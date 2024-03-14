from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook

config_dir = "playbooks/group_vars"


class Python:
    CONFIG_FILES = ["pythonwebservers.yml"]

    def __init__(self, environment="local"):
        self.configs = {}
        self.environment = environment
        self.file_manager = FileManager()
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
        run_playbook("python_webservers.yml", self.environment)
