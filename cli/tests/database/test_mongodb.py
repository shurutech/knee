from src.database.mongodb import Mongodb
from src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch

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
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_write_to_file):
        mongodb = Mongodb()
        Mongodb.configs = {
            "mongodbmainserver.yml": {
                'mongodb_database_name': 'myproject',
                'mongodb_database_password': 'dummy_password', 
                'mongodb_database_user': 'myuser', 
                'mongodb_version': 16
            }
        }
        mongodb.write_configuration_to_file()
        mock_write_to_file.assert_called_once_with('playbooks/group_vars', 'mongodbmainserver.yml', Mongodb.configs["mongodbmainserver.yml"])