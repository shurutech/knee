import yaml
import os

CONFIG_FILES = [
    "all.yml",
    "webservers.yml",
    "pythonwebservers.yml",
    "postgresmainserver.yml",
]

STAGING_HOSTS_DIR = "inventories/staging"
PRODUCTION_HOSTS_DIR = "inventories/production"

IMPACTED_HOST_GROUPS = ["webservers", "pythonwebservers", "postgresmainserver"]


class PythonPostgres:
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.configs = {}
        self.inventory = {}
        self.environment = environment
        for config_file in CONFIG_FILES:
            with open(os.path.join(config_dir, config_file)) as file:
                self.configs[config_file] = yaml.safe_load(file)

    def check_hosts(self, file_path=os.path.join(STAGING_HOSTS_DIR, "hosts.yml"), default_ip="192.168.181.128"):
        hosts = {}
        with open(file_path, "r") as file:
            hosts = yaml.safe_load(file)
            for group, group_info in hosts.items():
                for host, host_info in group_info["hosts"].items():
                    ansible_host = host_info.get("ansible_host")
                    if group in IMPACTED_HOST_GROUPS and ansible_host == default_ip:
                        raise ValueError(
                            f"Host: {host}, Ansible Host: {ansible_host} is set to default IP. Please set the ansible_host for the host."
                        )
        return True

    def check_defaults(self):
        for config_file, config in self.configs.items():
            print(f"Checking {config_file}...")
            print(config)
        print("Checking hosts file...")
        if self.environment == "staging":
            self.check_hosts(os.path.join(STAGING_HOSTS_DIR, "hosts.yml"))
        else:
            self.check_hosts(os.path.join(PRODUCTION_HOSTS_DIR, "hosts.yml"))
