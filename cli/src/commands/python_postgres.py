from InquirerPy import inquirer
from src.utils.utils import read_from_file, hosts_configuration_parameters, node_configuration_parameters, write_to_file
from src.webserver.python import Python
from src.database.postgresql import Postgresql

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

        
class PythonPostgres(Python, Postgresql):
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.configs = {}
        self.inventory = {}
        self.hosts = {}
        self.environment = environment
        self.hosts = read_from_file(dir_path[environment], "hosts.yml")    
        postgres_replica_server_acceptance = inquirer.confirm(message="Do you want to setup a replica server? (Default= No) :: ", default=False).execute()
        if postgres_replica_server_acceptance:
            IMPACTED_HOST_GROUPS.append("databasereplicaservers")
        for config_file in CONFIG_FILES:
                self.configs[config_file] = read_from_file(config_dir, config_file)
        self.server = Python()
        self.database = Postgresql(postgres_replica_server_acceptance)

    def check_hosts(self):
        self.hosts = hosts_configuration_parameters(IMPACTED_HOST_GROUPS, self.hosts)

    def check_configs(self):
        self.configs = node_configuration_parameters(self.configs)
        self.server.parameter_configuration()
        self.database.parameter_configuration()

    def write_configuration_and_run_playbook(self):
        write_to_file(dir_path[self.environment], "hosts.yml", self.hosts)
        for config_file in CONFIG_FILES:
            write_to_file("playbooks/group_vars", config_file, self.configs[config_file])
        # self.database.write_configuration_and_run_playbook()
        self.server.write_configuration_and_run_playbook()

    def check_defaults(self):
        self.check_configs()
        self.check_hosts()
        configuration_acceptance = inquirer.confirm(message="Do you want to change the configuration? (Default= Yes) :: ", default=True).execute()
        if configuration_acceptance:
            self.write_configuration_and_run_playbook()

    