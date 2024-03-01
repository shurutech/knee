from utils.utils import node_configuration_parameters
from utils.utils import read_from_file

config_dir = "playbooks/group_vars"

class Postgresql:
    config_files = ["postgresmainserver.yml"]
    configs = {}
    def __init__(self, replica_server_acceptance=False):
        if replica_server_acceptance:
            Postgresql.config_files.append("postgresreplicaservers.yml")  
        for config_file in Postgresql.config_files:
                Postgresql.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        print(Postgresql.configs)
        Postgresql.configs = node_configuration_parameters(Postgresql.configs)
