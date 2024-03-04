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