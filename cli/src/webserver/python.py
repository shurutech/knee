from src.utils.utils import node_configuration_parameters, read_from_file, write_to_file

config_dir = "playbooks/group_vars"


class Python:
    CONFIG_FILES = ["pythonwebservers.yml"]

    def __init__(self):
        self.configs = {}
        for config_file in self.CONFIG_FILES:
            self.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        self.configs = node_configuration_parameters(self.configs)

    def write_configuration_to_file(self):
        for config_file in self.CONFIG_FILES:
            write_to_file(config_dir, config_file, self.configs[config_file])
