from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager
from src.utils.runner import run_playbook

config_dir = "playbooks/group_vars"


class Golang:
    config_files = ["golangwebservers.yml"]
    configs = {}

    def __init__(self, environment="local"):
        self.environment = environment
        self.file_manager = FileManager()
        for config_file in self.config_files:
            self.configs[config_file] = self.file_manager.read_from_file(
                config_dir, config_file
            )

    def parameter_configuration(self):
        self.configs = load_configuration(self.configs)

    def write_configuration_and_run_playbook(self):
        for config_file in self.config_files:
            self.file_manager.write_to_file(
                config_dir, config_file, self.configs[config_file]
            )
        run_playbook("golang_server.yml", self.environment)
