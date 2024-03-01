from utils.utils import node_configuration_parameters
from utils.utils import read_from_file
config_dir = "playbooks/group_vars"
class Golang:
    config_files = ["golangwebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Golang.config_files:
                Golang.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        print("golang")
        Golang.configs = node_configuration_parameters(Golang.configs)
