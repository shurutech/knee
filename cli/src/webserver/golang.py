from src.utils.utils import node_configuration_parameters, read_from_file, write_to_file

config_dir = "playbooks/group_vars"
class Golang:
    config_files = ["golangwebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Golang.config_files:
                Golang.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        Golang.configs = node_configuration_parameters(Golang.configs)

    def write_configuration_to_file(self):
        for config_file in Golang.config_files:
            write_to_file(config_dir, config_file, Golang.configs[config_file])
