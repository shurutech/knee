from InquirerPy import inquirer
from src.utils.file_manager import FileManager
from src.utils.utils import (
    get_hosts_configuration_parameters,
    load_configuration,
)
from src.webservers.python import Python
from src.databases.postgresql import Postgresql
from src.webservers.golang import Golang
from src.databases.mongodb import Mongodb
from src.webservers.nodejs import Nodejs
from src.databases.mysql import Mysql
from src.webservers.ruby import Ruby
from src.caching_tools.redis import Redis
from src.utils.constants.constants import DIRECTORY_PATH, VARIABLE_DIR_PATH
from src.utils.constants.prompt import Prompt
from src.utils.constants.enum import Environment, HostGroup


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

class SystemFramework:
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
        self.selected_host_groups = self.get_selected_host_groups()
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
        self.default_hosts[HostGroup.DATABASE_REPLICA_SERVER.value] = {
            'hosts': replicas
        }

    def get_selected_host_groups(self):
        host_group_mapping = {
            self.is_replica_required: HostGroup.DATABASE_REPLICA_SERVER,
            self.database: HostGroup.DATABASE_MAIN_SERVER,
            self.webserver: HostGroup.WEB_SERVER,
            self.caching_tool: HostGroup.REDIS_SERVER
        }
        selected_host_groups = [host_group.value for selected_option, host_group in host_group_mapping.items() if selected_option]
        return selected_host_groups

    def load_generic_configuration(self):
        configs = {}
        for config_file in self.CONFIG_FILES:
            configs[config_file] = self.file_manager.read_from_file(VARIABLE_DIR_PATH, config_file)
        return configs

    def set_hosts(self):
        self.default_hosts = get_hosts_configuration_parameters(self.selected_host_groups, self.default_hosts)

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
                VARIABLE_DIR_PATH, config_file, self.configs[config_file]
            )
        if self.database:
            self.database_obj.apply_configuration()
        if self.webserver:
            self.webserver_obj.apply_configuration()
        if self.caching_tool:
            self.caching_tool_obj.apply_configuration()

    def setup(self):
        try:
            self.set_configs()
            self.set_hosts()
            configuration_confirmation = inquirer.confirm(
                message=Prompt.CONFIGURATION_SETUP_CHANGE.value,
                default=True,
            ).execute()
            if configuration_confirmation:
                self.apply_configuration()
            return True
        except Exception:
            return False
            