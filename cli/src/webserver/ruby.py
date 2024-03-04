from src.utils.utils import node_configuration_parameters, read_from_file
config_dir = "playbooks/group_vars"
class Ruby:
    config_files = ["rubywebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Ruby.config_files:
                Ruby.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        print("Ruby")
        Ruby.configs = node_configuration_parameters(Ruby.configs)
