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
from constants import DIRECTORY_PATH


class_map = {
    'python': Python,
    'postgresql': Postgresql,
    'golang': Golang,
    'mongodb': Mongodb,
    'nodejs': Nodejs,
    'mysql': Mysql,
    'ruby': Ruby
}

db_replica_map = {
    'postgresql': 1,
    'mysql': 1,
    'mongodb': 2
}


class CustomSelections:
    CONFIG_FILES = ["all.yml"]
    
    def __init__(self, environment="staging", config_dir="playbooks/group_vars", db_client_class=None, server_class=None):
        self.environment = environment
        self.file_manager = FileManager()
        self.server_class = self.get_class(server_class)
        self.db_class = self.get_class(db_client_class)
        self.replica_server_acceptance = self.get_confirmation_to_setup_replica_server() if self.db_class else False
        self.hosts = self.load_hosts_based_on_environment()
        self.replica_host_group = self.get_replica_host_group(db_client_class) if self.replica_server_acceptance else None
        self.impacted_host_groups = self.get_impacted_host_groups()
        self.configs = self.load_generic_configuration(config_dir)
        if self.db_class:
            self.database = self.db_class(self.replica_server_acceptance, self.environment)
        if self.server_class:
            self.server = self.server_class(self.environment)

    def load_hosts_based_on_environment(self):
        return self.file_manager.read_from_file(DIRECTORY_PATH[self.environment], "hosts.yml")
    
    def get_class(self, class_name):
        return class_map[class_name] if class_name in class_map else None

    def get_confirmation_to_setup_replica_server(self):
        return inquirer.confirm(
            message="Do you want to setup a replica server? (Default= No) :: ",
            default=False,
        ).execute()
    
    def get_replica_host_group(self, db_client_class):
        num_of_replica = db_replica_map[db_client_class] if db_client_class in db_replica_map else 0
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
        if hasattr(self, 'server'):
            self.server.parameter_configuration()
        if hasattr(self, 'database'):
            self.database.parameter_configuration()

    def write_configuration_and_run_playbook(self):
        self.file_manager.write_to_file(DIRECTORY_PATH[self.environment], "hosts.yml", self.hosts)
        for config_file in self.configs:
            self.file_manager.write_to_file(
                "playbooks/group_vars", config_file, self.configs[config_file]
            )
        if hasattr(self, 'database'):
            self.database.write_configuration_and_run_playbook()
        if hasattr(self, 'server'):
            self.server.write_configuration_and_run_playbook()

    def check_defaults(self):
        self.check_configs()
        self.check_hosts()
        configuration_acceptance = inquirer.confirm(
            message="Do you want to change the configuration? (Default= Yes) :: ",
            default=True,
        ).execute()
        if configuration_acceptance:
            self.write_configuration_and_run_playbook()

