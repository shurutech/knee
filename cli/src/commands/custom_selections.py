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

class CustomSelections:
    CONFIG_FILES = ["all.yml"]
    REPLICA_CONFIG_FILES = ["all.yml", "databasereplicaservers.yml"]
    
    def __init__(self, environment="staging", config_dir="playbooks/group_vars", db_client_class=None, server_class=None):
        self.configs = {}
        self.inventory = {}
        self.hosts = {}
        self.impacted_host_groups = []
        self.environment = environment
        self.file_manager = FileManager()
        replica_server_acceptance = False
        self.hosts = self.file_manager.read_from_file(DIRECTORY_PATH[environment], "hosts.yml")
        server_class = class_map[server_class] if server_class is not None else None
        db_class = class_map[db_client_class] if db_client_class is not None else None
        if server_class is not None:
            self.impacted_host_groups.append("webservers")
        if db_class is not None:
            self.impacted_host_groups.append("databasemainserver")
            replica_server_acceptance = inquirer.confirm(
                message="Do you want to setup a replica server? (Default= No) :: ",
                default=False,
            ).execute()
        self.config_files = self.CONFIG_FILES if not replica_server_acceptance else self.REPLICA_CONFIG_FILES
        if replica_server_acceptance:
            self.impacted_host_groups.append("databasereplicaservers")
        for config_file in self.config_files:
            self.configs[config_file] = self.file_manager.read_from_file(config_dir, config_file)
        if db_class:
            self.database = db_class(replica_server_acceptance, self.environment)
        if server_class:
            self.server = server_class(self.environment)

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
        for config_file in self.config_files:
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

