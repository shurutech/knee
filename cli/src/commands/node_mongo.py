from InquirerPy import inquirer
from src.utils.utils import (
    hosts_configuration_parameters,
    load_configuration,
)
from src.webserver.nodejs import Nodejs
from src.database.mongodb import Mongodb
from constants import DIRECTORY_PATH
from src.utils.file_manager import FileManager

CONFIG_FILES = [
    "all.yml",
    "webservers.yml",
]

IMPACTED_HOST_GROUPS = ["webservers", "databasemainserver"]


class NodeMongo(Nodejs, Mongodb):
    def __init__(self, environment="staging", config_dir="playbooks/group_vars"):
        self.configs = {}
        self.inventory = {}
        self.hosts = {}
        self.environment = environment
        self.file_manager = FileManager()
        self.hosts = self.file_manager.read_from_file(DIRECTORY_PATH[environment], "hosts.yml")
        postgres_replica_server_acceptance = inquirer.confirm(
            message="Do you want to setup a replica server? (Default= No) :: ",
            default=False,
        ).execute()
        if postgres_replica_server_acceptance:
            IMPACTED_HOST_GROUPS.append("databasereplicaservers")
        for config_file in CONFIG_FILES:
            self.configs[config_file] = self.file_manager.read_from_file(config_dir, config_file)
        self.server = Nodejs(environment)
        self.database = Mongodb(postgres_replica_server_acceptance, environment)

    def check_hosts(self):
        self.hosts = hosts_configuration_parameters(IMPACTED_HOST_GROUPS, self.hosts)

    def check_configs(self):
        self.configs = load_configuration(self.configs)
        self.server.parameter_configuration()
        self.database.parameter_configuration()

    def write_configuration_and_run_playbook(self):
        self.file_manager.write_to_file(DIRECTORY_PATH[self.environment], "hosts.yml", self.hosts)
        for config_file in CONFIG_FILES:
            self.file_manager.write_to_file(
                "playbooks/group_vars", config_file, self.configs[config_file]
            )
        self.database.write_configuration_and_run_playbook()
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
