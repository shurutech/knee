from InquirerPy import inquirer
from src.utils.file_manager import FileManager
from src.utils.utils import (
    hosts_configuration_parameters,
    load_configuration,
)
from src.webserver.python import Python
from src.database.postgresql import Postgresql
from src.webserver.golang import Golang
from src.database.mongodb import Mongodb
from src.webserver.nodejs import Nodejs
from src.database.mysql import Mysql
from src.webserver.ruby import Ruby
from src.caching_tools.redis import Redis
from constants import DIRECTORY_PATH
from src.utils.constants.prompt import Prompt
from src.utils.constants.enum import Environment


class_map = {
    'python': Python,
    'postgresql': Postgresql,
    'golang': Golang,
    'mongodb': Mongodb,
    'nodejs': Nodejs,
    'mysql': Mysql,
    'ruby': Ruby,
    'redis': Redis
}

default_db_replica_count = {
    'postgresql': 1,
    'mysql': 1,
    'mongodb': 2
}

REPLICA_CONFIG = {
            'ansible_connection': 'ssh',
            'ansible_host': '192.168.181.129',
            'ansible_port': 22,
            'ansible_ssh_private_key_file': '.vagrant/machines/vm2/vmware_fusion/private_key',
            'ansible_user': 'vagrant',
        }

config_dir = "playbooks/group_vars"


class CustomSystem:
    CONFIG_FILES = ["all.yml"]
    
    def __init__(self, user_selections, environment=Environment.LOCAL.value):
        self.environment = environment
        self.file_manager = FileManager()
        self.webserver = self.get_class(user_selections.get("webserver"))
        self.database = self.get_class(user_selections.get('database'))
        self.caching_tool = self.get_class(user_selections.get("caching_tool"))
        self.is_replica_required = self.get_replica_setup_confirmation() if self.database else False
        self.default_hosts = self.load_hosts()
        self.replica_host_group = self.get_replica_host_group(user_selections.get('database')) if self.is_replica_required else None
        self.impacted_host_groups = self.get_selected_host_groups()
        self.configs = self.load_generic_configuration()
        self.database_obj = self.database(self.is_replica_required, self.environment) if self.database else None
        self.webserver_obj = self.webserver(self.environment) if self.webserver else None
        self.caching_tool_obj = self.caching_tool(self.environment) if self.caching_tool else None

    def load_hosts(self):
        return self.file_manager.read_from_file(DIRECTORY_PATH[self.environment], "hosts.yml")
    
    def get_class(self, class_name):
        return class_map[class_name] if class_name in class_map else None

    def get_replica_setup_confirmation(self):
        return inquirer.confirm(
            message=Prompt.REPLICA_SETUP.value,
            default=False,
        ).execute()
    
    def get_replica_host_group(self, database):
        num_of_replica = default_db_replica_count[database] if database in default_db_replica_count else 0
        replicas = {}
        for replica_count in range(1, num_of_replica + 1):
           replica_name = f"replica{replica_count}"
           replicas[replica_name] = dict(REPLICA_CONFIG)
        self.default_hosts['databasereplicaservers'] = {
            'hosts': replicas
        }

    def get_selected_host_groups(self):
        host_groups = []
        if self.is_replica_required:
            host_groups.append("databasereplicaservers")
        if self.database:
            host_groups.append("databasemainserver")
        if self.webserver:
            host_groups.append("webservers")
        if self.caching_tool:
            host_groups.append("redisservers")
        return host_groups

    def load_generic_configuration(self):
        configs = {}
        for config_file in self.CONFIG_FILES:
            configs[config_file] = self.file_manager.read_from_file(config_dir, config_file)
        return configs

    def set_hosts(self):
        self.default_hosts = hosts_configuration_parameters(self.impacted_host_groups, self.default_hosts)

    def set_configs(self):
        self.configs = load_configuration(self.configs)
        if self.webserver:
            self.webserver_obj.update_configuration()
        if self.database:
            self.database_obj.update_configuration()
        if self.caching_tool:
            self.caching_tool_obj.update_configuration()

    def apply_configuration(self):
        self.file_manager.write_to_file(DIRECTORY_PATH[self.environment], "hosts.yml", self.default_hosts)
        for config_file in self.configs:
            self.file_manager.write_to_file(
                config_dir, config_file, self.configs[config_file]
            )
        if self.database:
            self.database_obj.apply_configuration()
        if self.webserver:
            self.webserver_obj.apply_configuration()
        if self.caching_tool:
            self.caching_tool_obj.apply_configuration()

    def check_defaults(self):
        self.set_configs()
        self.set_hosts()
        configuration_acceptance = inquirer.confirm(
            message=Prompt.CONFIGURATION_SETUP_CHANGE.value,
            default=True,
        ).execute()
        if configuration_acceptance:
            self.apply_configuration()

