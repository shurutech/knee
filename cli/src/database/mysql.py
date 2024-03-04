from src.utils.utils import node_configuration_parameters, read_from_file

config_dir = "playbooks/group_vars"

class Mysql:
    config_files = ["mysqlmainserver.yml"]
    configs = {}
    def __init__(self, replica_server_acceptance=False):
        if replica_server_acceptance:
            Mysql.config_files.append("mysqlreplicaservers.yml")  
        for config_file in Mysql.config_files:
                Mysql.configs[config_file] = read_from_file(config_dir, config_file)

    def parameter_configuration(self):
        Mysql.configs = node_configuration_parameters(Mysql.configs)
 