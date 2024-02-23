import yaml
import os
from pprint import pprint
import typer
from rich.progress import track
import time
from colorama import Fore, Style
import getpass

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
            # print(os.path)
            with open(os.path.join(config_dir, config_file)) as file:
                self.configs[config_file] = yaml.safe_load(file)

    def check_hosts(self, file_path=os.path.join(STAGING_HOSTS_DIR, "hosts.yml"), default_ip="192.168.181.128"):
        hosts = {}
        with open(file_path, "r") as file:
            hosts = yaml.safe_load(file)
            # print(hosts)
            for group, group_info in hosts.items():
                for host, host_info in group_info["hosts"].items():
                    ansible_host = host_info.get("ansible_host")
                    if group in IMPACTED_HOST_GROUPS and ansible_host == default_ip:
                        raise ValueError(
                            f"Host: {host}, Ansible Host: {ansible_host} is set to default IP. Please set the ansible_host for the host."
                        )
        return True

    def check_configs(self):
        print("config/....................")
        configs = {}
        # pprint(self.configs)
        for groups, groups_value in self.configs.items():
            if groups not in configs:
                configs[groups] = {}
            for key, value in groups_value.items():
                configs[groups][key] = input(f"💼 Enter {key}: (Default: {value}) :: ") or value 

        print("\n Default values: \n")  
        for groups, groups_value in configs.items():
            for key, value in groups_value.items():
                if value == self.configs[groups][key]:
                    flag: bool = input(f"{Fore.RED} Do you want to keep the default value for {key}? (y/n) ::  {Style.RESET_ALL}").lower()
                    while True:
                     if flag in ['y','n']: 
                        if flag == 'n':
                            configs[groups][key] = input(f"💼 Enter {key}: (Default: {value}) :: ") or value
                        break
                     else:
                        flag = input(f"💼 Do you want to keep the default value for {key}? (y/n) :: ")   



    def check_defaults(self):
        # for config_file, config in self.configs.items():
            # print(f"Checking {config_file}...")
            # print(config)
        # print("Checking hosts file...")
        self.check_configs()
        # if self.environment == "staging":
        #     self.check_hosts(os.path.join(STAGING_HOSTS_DIR, "hosts.yml"))
        # else:
        #     self.check_hosts(os.path.join(PRODUCTION_HOSTS_DIR, "hosts.yml"))
