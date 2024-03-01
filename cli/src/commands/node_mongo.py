from InquirerPy import inquirer
from cli.src.utils.utils import read_from_file, hosts_configuration_parameters, node_configuration_parameters
from cli.src.webserver.nodejs import Nodejs
from cli.src.database.mongodb import Mongodb

CONFIG_FILES = [
    "all.yml",
    "webservers.yml",
]

LOCAL_HOSTS_DIR = "inventories/local"
STAGING_HOSTS_DIR = "inventories/staging"
PRODUCTION_HOSTS_DIR = "inventories/production"

dir_path = {
     "staging": STAGING_HOSTS_DIR,
     "local": LOCAL_HOSTS_DIR,
     "production": PRODUCTION_HOSTS_DIR
}

IMPACTED_HOST_GROUPS = [
     "webservers",
     "pythonwebservers", 
     "postgresmainserver"
]


        
class NodeMongo(Nodejs, Mongodb):
    configs = {}
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.inventory = {}
        self.hosts = {}
        self.environment = environment
        self.hosts = read_from_file(dir_path[environment], "hosts.yml")    
        postgres_replica_server_acceptance = inquirer.confirm(message="Do you want to setup a replica server? (Default= No) :: ", default=False).execute()
        if postgres_replica_server_acceptance:
            IMPACTED_HOST_GROUPS.append("postgresreplicaservers")
        for config_file in CONFIG_FILES:
                NodeMongo.configs[config_file] = read_from_file(config_dir, config_file)
        Nodejs.__init__(self)       
        Mongodb.__init__(self, postgres_replica_server_acceptance)

    def check_hosts(self):
        self.hosts = hosts_configuration_parameters(IMPACTED_HOST_GROUPS, self.environment, dir_path, self.hosts)

    def check_configs(self):
        NodeMongo.configs = node_configuration_parameters(NodeMongo.configs)
        Nodejs.parameter_configuration(self)
        Mongodb.parameter_configuration(self)

    def check_defaults(self):
        self.check_configs()
        self.check_hosts()
