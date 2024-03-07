from src.commands.golang_mongo import GolangMongo, IMPACTED_HOST_GROUPS, CONFIG_FILES
from unittest.mock import MagicMock, patch
import unittest

class TestGolangMongo(unittest.TestCase):
    @patch("src.commands.golang_mongo.inquirer.confirm")
    def test_init_with_replica_server_acceptance_true(self, mock_confirm):
        mock_confirm.return_value.execute.return_value = True
        GolangMongo()
        assert "databasereplicaservers" in IMPACTED_HOST_GROUPS
    
    @patch("src.commands.golang_mongo.inquirer.confirm")
    def test_init_with_replica_server_acceptance_false(self, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        GolangMongo()
        assert "databasereplicaservers" not in IMPACTED_HOST_GROUPS

    @patch("src.commands.golang_mongo.inquirer.confirm")
    @patch("src.commands.golang_mongo.hosts_configuration_parameters")
    def test_check_hosts(self, mock_hosts_configurations_parameters, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        golang_mongo = GolangMongo()
        golang_mongo.hosts = {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.12.1/23"
                    }
                }
            }
        }
        golang_mongo.check_hosts()
        expected_args = (IMPACTED_HOST_GROUPS,  {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.12.1/23"
                    }
                }
            }
        })
        mock_hosts_configurations_parameters.assert_called_once_with(*expected_args)
    
    @patch("src.commands.golang_mongo.write_to_file")
    @patch("src.commands.golang_mongo.inquirer.confirm")
    def test_write_configuration_to_file_when_it_is_called(self, mock_confirm, mock_write_to_file):
        mock_confirm.return_value.execute.return_value = False
        golang_mongo = GolangMongo()
        golang_mongo.database = MagicMock()
        golang_mongo.server = MagicMock()
        golang_mongo.environment = "staging"
        golang_mongo.hosts = {"test": "test"}
        golang_mongo.write_configuration_to_file()
        assert mock_write_to_file.called


    @patch("src.commands.golang_mongo.inquirer.confirm")
    @patch("src.commands.golang_mongo.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_config, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        golang_mongo = GolangMongo()
        golang_mongo.database = MagicMock()
        golang_mongo.server = MagicMock()
        golang_mongo.environment = "staging"
        golang_mongo.hosts = {"test": "test"}
        golang_mongo.write_configuration_to_file()
        assert mock_write_config.call_count == 1 + CONFIG_FILES.__len__()
    
    @patch("src.commands.golang_mongo.inquirer.confirm")
    @patch("src.commands.golang_mongo.node_configuration_parameters")
    @patch("src.commands.golang_mongo.Mongodb.parameter_configuration")
    @patch("src.commands.golang_mongo.Golang.parameter_configuration")
    def test_check_configs(self, mock_golang_parameter_configuration, mock_mongodb_parameter_configuration, mock_node_configuration_parameters, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        golang_mongo = GolangMongo()
        golang_mongo.check_configs()
        assert mock_golang_parameter_configuration.called
        assert mock_mongodb_parameter_configuration.called
        assert mock_node_configuration_parameters.called

    @patch("src.commands.golang_mongo.inquirer.confirm")
    @patch("src.commands.golang_mongo.GolangMongo.check_configs")
    @patch("src.commands.golang_mongo.GolangMongo.check_hosts")
    @patch("src.commands.golang_mongo.GolangMongo.write_configuration_to_file")
    def test_check_defaults_with_configuration_when_acceptance_is_true(self, mock_write_configuration_to_file ,mock_check_hosts, mock_check_configs, mock_confirm):
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: True)]
        golang_mongo = GolangMongo()
        golang_mongo.check_defaults()
        assert mock_check_hosts.called
        assert mock_check_configs.called
        assert mock_write_configuration_to_file.called

    @patch("src.commands.golang_mongo.inquirer.confirm")
    @patch("src.commands.golang_mongo.GolangMongo.check_configs")
    @patch("src.commands.golang_mongo.GolangMongo.check_hosts")
    @patch("src.commands.golang_mongo.GolangMongo.write_configuration_to_file")
    def test_check_defaults_with_configuration_when_acceptance_is_false(self, mock_write_configuration_to_file ,mock_check_hosts, mock_check_configs, mock_confirm):
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        golang_mongo = GolangMongo()
        golang_mongo.database = MagicMock()
        golang_mongo.server = MagicMock()
        golang_mongo.check_defaults()
        assert mock_check_hosts.called
        assert mock_check_configs.called
        assert not mock_write_configuration_to_file.called

    