from src.utils.utils import load_configuration
from src.utils.file_manager import FileManager

config_dir = "playbooks/group_vars"


class Ruby:
    config_files = ["rubywebservers.yml"]
    configs = {}

    def __init__(self):
        self.file_manager = FileManager()
        for config_file in Ruby.config_files:
            Ruby.configs[config_file] = self.file_manager.read_from_file(
                config_dir, config_file
            )

    def parameter_configuration(self):
        Ruby.configs = load_configuration(Ruby.configs)
