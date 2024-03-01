from utils.utils import node_configuration_parameters
from utils.utils import read_from_file

config_dir = "playbooks/group_vars"

class Mongodb:
    config_files = ["mongodbmainserver.yml"]
    configs = {}
    def __init__(self, replica_server_acceptance=False):
        if replica_server_acceptance:
            Mongodb.config_files.append("mongodbreplicaservers.yml")  
        for config_file in Mongodb.config_files:
                Mongodb.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        print(Mongodb.configs)
        Mongodb.configs = node_configuration_parameters(Mongodb.configs)
