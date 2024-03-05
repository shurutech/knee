from InquirerPy import inquirer
from src.utils.utils import read_from_file, hosts_configuration_parameters, node_configuration_parameters
from src.webserver.golang import Golang
from src.database.mongodb import Mongodb

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
        "databasemainserver"
    ]

class GolangMongo(Golang, Mongodb):
    configs = {}
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.inventory = {}
        self.hosts = {}
        self.environment = environment
        self.hosts = read_from_file(dir_path[environment], "hosts.yml")    
        postgres_replica_server_acceptance = inquirer.confirm(message="Do you want to setup a replica server? (Default= No) :: ", default=False).execute()
        if postgres_replica_server_acceptance:
            IMPACTED_HOST_GROUPS.append("databasereplicaservers")
        for config_file in CONFIG_FILES:
                GolangMongo.configs[config_file] = read_from_file(config_dir, config_file)
        Golang.__init__(self)       
        Mongodb.__init__(self, postgres_replica_server_acceptance)

    def check_hosts(self):
        self.hosts = hosts_configuration_parameters(IMPACTED_HOST_GROUPS, self.hosts)

    def check_configs(self):
        GolangMongo.configs = node_configuration_parameters(GolangMongo.configs)
        Golang.parameter_configuration(self)
        Mongodb.parameter_configuration(self)

    def check_defaults(self):
        self.check_configs()
        self.check_hosts()