from src.utils.utils import node_configuration_parameters, read_from_file, write_to_file

config_dir = "playbooks/group_vars"
class Golang:
    config_files = ["golangwebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in self.config_files:
                self.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        self.configs = node_configuration_parameters(self.configs)

    def write_configuration_to_file(self):
        for config_file in self.config_files:
            write_to_file(config_dir, config_file, self.configs[config_file])
