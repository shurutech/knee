from src.databases.mongodb import Mongodb
from src.utils.utils import load_configuration
import unittest
from unittest.mock import patch, call


class TestMongodb(unittest.TestCase):
    def test_update_configuration_with_default_values(self):
        mongodb = Mongodb()
        mongodb.configs = {"mongodbmainserver.yml": {"mongodb_port": "27017"}}
        with patch("builtins.input", return_value=""):
            mongodb.configs = load_configuration(mongodb.configs)
        self.assertEqual(
            mongodb.configs["mongodbmainserver.yml"]["mongodb_port"], "27017"
        )

    def test_update_configuration_with_user_input(self):
        mongodb = Mongodb()
        mongodb.configs = {"mongodbmainserver.yml": {"mongodb_port": "27017"}}
        with patch("builtins.input", return_value="27018"):
            mongodb.configs = load_configuration(mongodb.configs)
        self.assertEqual(
            mongodb.configs["mongodbmainserver.yml"]["mongodb_port"], "27018"
        )

    def test_update_configuration_when_is_replica_required_true(self):
        mongodb = Mongodb(True)
        mongodb.configs = {
            "mongodbwebservers.yml": {"mongodb_port": "27017"},
            "mongodbreplicaservers.yml": {"mongodb_port": "27017"},
        }
        with patch("builtins.input", side_effect=["27018", "27019"]):
            mongodb.configs = load_configuration(mongodb.configs)
        self.assertEqual(
            mongodb.configs["mongodbwebservers.yml"]["mongodb_port"], "27018"
        )
        self.assertEqual(
            mongodb.configs["mongodbreplicaservers.yml"]["mongodb_port"], "27019"
        )

    @patch("src.databases.mongodb.FileManager.write_to_file")
    @patch("src.databases.mongodb.run_playbook")
    def test_apply_configuration_called_with_expected_arguments(
        self, mock_run_playbook, mock_write_to_file
    ):
        mongodb = Mongodb()
        mongodb.environment = "local"
        mongodb.config_files = ["mongodbmainserver.yml"]
        mongodb.configs = {
            "mongodbmainserver.yml": {
                "mongodb_database_name": "myproject",
            }
        }
        mongodb.apply_configuration()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "mongodbmainserver.yml",
            mongodb.configs["mongodbmainserver.yml"],
        )
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with(
            "mongodb_server.yml", mongodb.environment
        )
