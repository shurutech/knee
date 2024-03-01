from utils.utils import node_configuration_parameters
from utils.utils import read_from_file
config_dir = "playbooks/group_vars"
class Nodejs:
    config_files = ["nodewebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Nodejs.config_files:
                Nodejs.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        print("Node")
        Nodejs.configs = node_configuration_parameters(Nodejs.configs)
