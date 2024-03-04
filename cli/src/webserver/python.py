from src.utils.utils import node_configuration_parameters, read_from_file
config_dir = "playbooks/group_vars"
class Python:
    config_files = ["pythonwebservers.yml"]
    configs = {}
    def __init__(self):
        for config_file in Python.config_files:
                Python.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        Python.configs = node_configuration_parameters(Python.configs)

