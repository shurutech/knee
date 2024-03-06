from src.utils.utils import node_configuration_parameters, read_from_file, write_to_file
config_dir = "playbooks/group_vars"
class Nodejs:
    config_files = ["nodewebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Nodejs.config_files:
                Nodejs.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        Nodejs.configs = node_configuration_parameters(Nodejs.configs)

    def write_configuration_to_file(self):
        for config_file in Nodejs.config_files:
            write_to_file(config_dir, config_file, Nodejs.configs[config_file])    
   
    
