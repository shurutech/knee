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
from src.additional_services.redis import Redis
from constants import DIRECTORY_PATH
import src.utils.constants.message_constants as MESSAGE


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

db_replica_count = {
    'postgresql': 1,
    'mysql': 1,
    'mongodb': 2
}


class CustomSelections:
    CONFIG_FILES = ["all.yml"]
    
    def __init__(self, environment="staging", config_dir="playbooks/group_vars", db_client_class=None, server_class=None, additional_service=None):
        self.environment = environment
        self.file_manager = FileManager()
        self.server_class = self.get_class(server_class)
        self.db_class = self.get_class(db_client_class)
        self.additional_service = self.get_class(additional_service)
        self.replica_server_acceptance = self.get_replica_setup_confirmation() if self.db_class else False
        self.hosts = self.load_hosts()
        self.replica_host_group = self.get_replica_host_group(db_client_class) if self.replica_server_acceptance else None
        self.impacted_host_groups = self.get_impacted_host_groups()
        self.configs = self.load_generic_configuration(config_dir)
        if self.db_class:
            self.database = self.db_class(self.replica_server_acceptance, self.environment)
        if self.server_class:
            self.server = self.server_class(self.environment)
        if self.additional_service:
            self.additional_service = self.additional_service(self.environment)

    def load_hosts(self):
        return self.file_manager.read_from_file(DIRECTORY_PATH[self.environment], "hosts.yml")
    
    def get_class(self, class_name):
        return class_map[class_name] if class_name in class_map else None

    def get_replica_setup_confirmation(self):
        return inquirer.confirm(
            message=MESSAGE.REPLICA_SETUP_PROMPT,
            default=False,
        ).execute()
    
    def get_replica_host_group(self, db_client_class):
        num_of_replica = db_replica_count[db_client_class] if db_client_class in db_replica_count else 0
        replicas = {}
        for i in range(1, num_of_replica + 1):
           replica_name = f"replica{i}"
           replicas[replica_name] = {
            'ansible_connection': 'ssh',
            'ansible_host': '192.168.181.129',
            'ansible_port': 22,
            'ansible_ssh_private_key_file': '.vagrant/machines/vm2/vmware_fusion/private_key',
            'ansible_user': 'vagrant',
        }
        self.hosts['databasereplicaservers'] = {
            'hosts': replicas
        }

    def get_impacted_host_groups(self):
        host_groups = []
        if self.replica_server_acceptance:
            host_groups.append("databasereplicaservers")
        else:
            if self.db_class:
                host_groups.append("databasemainserver")
            if self.server_class:
                host_groups.append("webservers")
            if self.additional_service:
                host_groups.append("redisservers")
        return host_groups

    def load_generic_configuration(self, config_dir):
        configs = {}
        for config_file in self.CONFIG_FILES:
            configs[config_file] = self.file_manager.read_from_file(config_dir, config_file)
        return configs

    def check_hosts(self):
        self.hosts = hosts_configuration_parameters(self.impacted_host_groups, self.hosts)

    def check_configs(self):
        self.configs = load_configuration(self.configs)
        if self.server_class:
            self.server.parameter_configuration()
        if self.db_class:
            self.database.parameter_configuration()
        if self.additional_service:
            self.additional_service.parameter_configuration()

    def apply_configuration(self):
        self.file_manager.write_to_file(DIRECTORY_PATH[self.environment], "hosts.yml", self.hosts)
        for config_file in self.configs:
            self.file_manager.write_to_file(
                "playbooks/group_vars", config_file, self.configs[config_file]
            )
        if self.db_class:
            self.database.apply_configuration()
        if self.server_class:
            self.server.apply_configuration()
        if self.additional_service:
            self.additional_service.apply_configuration()

    def check_defaults(self):
        self.check_configs()
        self.check_hosts()
        configuration_acceptance = inquirer.confirm(
            message=MESSAGE.CONFIGURATION_SETUP_CHANGE_PROMPT,
            default=True,
        ).execute()
        if configuration_acceptance:
            self.apply_configuration()

