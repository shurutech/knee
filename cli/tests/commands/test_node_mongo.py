from src.commands.node_mongo import NodeMongo, CONFIG_FILES, IMPACTED_HOST_GROUPS
import unittest
from unittest.mock import patch, MagicMock

class TestNodeMongo(unittest.TestCase):
    @patch("src.commands.node_mongo.inquirer.confirm")
    def test_init_with_replica_server_acceptance_true(self, mock_confirm):
        mock_confirm.return_value.execute.return_value = True
        NodeMongo()
        assert "databasereplicaservers" in IMPACTED_HOST_GROUPS

    @patch("src.commands.node_mongo.inquirer.confirm")
    def test_init_with_replica_server_acceptance_false(self, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        NodeMongo()
        assert "databasereplicaservers" not in IMPACTED_HOST_GROUPS
    
    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch("src.commands.node_mongo.hosts_configuration_parameters")
    def test_check_hosts(self, mock_hosts_configurations_parameters, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        node_mongo = NodeMongo()
        node_mongo.hosts = {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.12.1/23"
                    }
                }
            }          
        }
        node_mongo.check_hosts()
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
   
    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch.object(NodeMongo, "write_configuration_to_file")
    def test_write_configuration_to_file_when_it_is_called(self, mock_write_to_file, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        node_mongo = NodeMongo()
        node_mongo.environment = "staging"
        node_mongo.hosts = {"test": "test"}
        node_mongo.write_configuration_to_file()
        assert mock_write_to_file.called

    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch("src.commands.node_mongo.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_config, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        node_mongo = NodeMongo()
        node_mongo.environment = "staging"
        node_mongo.hosts = {"test": "test"}
        node_mongo.write_configuration_to_file()
        assert mock_write_config.call_count == 1 + CONFIG_FILES.__len__()
    
    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch("src.commands.node_mongo.node_configuration_parameters")
    @patch("src.commands.node_mongo.Mongodb.parameter_configuration")
    @patch("src.commands.node_mongo.Nodejs.parameter_configuration")
    def test_check_configs(self, mock_node_parameter_configuration, mock_mongodb_parameter_configuration, mock_node_configuration_parameters, mock_confirm):
        mock_confirm.return_value.execute.return_value = False
        node_mongo = NodeMongo()
        node_mongo.check_configs()
        assert mock_node_parameter_configuration.called
        assert mock_mongodb_parameter_configuration.called
        assert mock_node_configuration_parameters.called

    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch("src.commands.node_mongo.NodeMongo.check_configs")
    @patch("src.commands.node_mongo.NodeMongo.check_hosts")
    @patch("src.commands.node_mongo.NodeMongo.write_configuration_to_file")
    def test_check_defaults_with_configuration_when_acceptance_is_true(self, mock_write_configuration_to_file ,mock_check_hosts, mock_check_configs, mock_confirm):
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: True)]
        node_mongo = NodeMongo()
        node_mongo.check_defaults()
        assert mock_check_hosts.called
        assert mock_check_configs.called
        assert mock_write_configuration_to_file.called

    @patch("src.commands.node_mongo.inquirer.confirm")
    @patch("src.commands.node_mongo.NodeMongo.check_configs")
    @patch("src.commands.node_mongo.NodeMongo.check_hosts")
    @patch("src.commands.node_mongo.NodeMongo.write_configuration_to_file")
    def test_check_defaults_with_configuration_when_acceptance_is_false(self, mock_write_configuration_to_file ,mock_check_hosts, mock_check_configs, mock_confirm):
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        node_mongo = NodeMongo()
        node_mongo.check_defaults()
        assert mock_check_hosts.called
        assert mock_check_configs.called
        assert not mock_write_configuration_to_file.called    
        

    

    

