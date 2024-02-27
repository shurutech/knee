import yaml
import os
from InquirerPy import inquirer

CONFIG_FILES = [
    "all.yml",
    "webservers.yml",
    "pythonwebservers.yml",
    "postgresmainserver.yml",
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


def get_user_input(key, default_value):
        return input(f"💼 Enter {key}: (Default: {default_value}) :: ") or default_value

def get_user_confirmation(key):
            user_confirmation = inquirer.confirm(message=f"Do you want to keep the default value for {key}?", default=True).execute()
            return user_confirmation == False

def write_to_file(directory, filename, data):
        with open(os.path.join(directory, filename), "w") as file:
            yaml.dump(data, file)

def read_from_file(directory, filename):
        with open(os.path.join(directory, filename), "r") as file:
            return yaml.safe_load(file)
        
class PythonPostgres:
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.configs = {}
        self.inventory = {}
        self.hosts = {}
        self.environment = environment
        self.hosts = read_from_file(dir_path[environment], "hosts.yml")    
        postgres_replica_server_acceptance = inquirer.confirm(message="Do you want to setup a replica server? (Default= No) :: ", default=False).execute()
        if postgres_replica_server_acceptance:
            CONFIG_FILES.append("postgresreplicaservers.yml")
            IMPACTED_HOST_GROUPS.append("postgresreplicaservers")
        for config_file in CONFIG_FILES:
                self.configs[config_file] = read_from_file(config_dir, config_file)

    def check_hosts(self):
            for group, group_info in self.hosts.items():  
                if group in IMPACTED_HOST_GROUPS:
                    for hosts, host_info in group_info["hosts"].items():
                        print(f"-----{group}--> {hosts} Configuration")
                        for key, value in host_info.items():
                            self.hosts[group]["hosts"][hosts][key] = get_user_input(key, value)
            write_to_file(dir_path[self.environment], "hosts.yml", self.hosts)

    def check_configs(self):
        print("config/....................")
        for group, group_values in self.configs.items():
            for key, value in group_values.items():
                self.configs[group][key] = get_user_input(key, value)
            write_to_file("playbooks/group_vars", group, self.configs[group])   


    def check_defaults(self):
        self.check_configs()
        self.check_hosts()
