from src.database.mongodb import Mongodb
from src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch, call

class TestMongodb(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        mongodb = Mongodb()
        mongodb.configs = {
            "mongodbmainserver.yml": {
                "mongodb_port": "27017"
            }
        }
        with patch("builtins.input", return_value=""):
            mongodb.configs = node_configuration_parameters(mongodb.configs)
        self.assertEqual(mongodb.configs["mongodbmainserver.yml"]["mongodb_port"], "27017")

    def test_parameter_configuration_with_user_input(self):
        mongodb = Mongodb()
        mongodb.configs = {
            "mongodbmainserver.yml": {
                "mongodb_port": "27017"
            }
        }
        with patch("builtins.input", return_value="27018"):
            mongodb.configs = node_configuration_parameters(mongodb.configs)
        self.assertEqual(mongodb.configs["mongodbmainserver.yml"]["mongodb_port"], "27018")
    
    def test_parameter_configuration_with_replica_server_acceptance(self):
        mongodb = Mongodb(True)
        mongodb.configs = {
            "mongodbwebservers.yml": {
                "mongodb_port": "27017"
            },
            "mongodbreplicaservers.yml": {
                "mongodb_port": "27017"
            }
        }
        with patch("builtins.input", side_effect=["27018", "27019"]):
            mongodb.configs = node_configuration_parameters(mongodb.configs)
        self.assertEqual(mongodb.configs["mongodbwebservers.yml"]["mongodb_port"], "27018")
        self.assertEqual(mongodb.configs["mongodbreplicaservers.yml"]["mongodb_port"], "27019")

    @patch("src.database.mongodb.write_to_file")
    @patch("src.database.mongodb.run_playbook")
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_run_playbook ,mock_write_to_file):
        mongodb = Mongodb()
        mongodb.environment = "local"
        mongodb.config_files = ["mongodbmainserver.yml"]
        mongodb.configs = {
            "mongodbmainserver.yml": {
                'mongodb_database_name': 'myproject',
            }
        }
        mongodb.write_configuration_to_file()
        actual_call = mock_write_to_file.call_args
        expected_call = call('playbooks/group_vars', 'mongodbmainserver.yml', mongodb.configs["mongodbmainserver.yml"])
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with('mongodb_server.yml', mongodb.environment)