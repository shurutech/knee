from src.database.postgresql import Postgresql
from src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch, call
class TestPostgresql(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        postgresql = Postgresql()
        postgresql.configs = {
            "mainserver.yml": {
                "postgresql_port": "5432"
            }
        }
        with patch("builtins.input", return_value=""):
            postgresql.configs = node_configuration_parameters(postgresql.configs)
        self.assertEqual(postgresql.configs["mainserver.yml"]["postgresql_port"], "5432")

    def test_parameter_configuration_with_user_input(self):
        postgresql = Postgresql()
        postgresql.configs = {
            "mainserver.yml": {
                "postgresql_port": "5432"
            }
        }
        with patch("builtins.input", return_value="5434"):
            postgresql.configs = node_configuration_parameters(postgresql.configs)
        self.assertEqual(postgresql.configs["mainserver.yml"]["postgresql_port"], "5434")
    
    def test_parameter_configuration_with_replica_server_acceptance(self):
        python = Postgresql(True)
        python.configs = {
            "postgresmainrvers.yml": {
                "python_port": "5432"
            },
            "postgresreplicaservers.yml": {
                "python_port": "5432"
            }
        }
        with patch("builtins.input", side_effect=["5434", "5000"]):
            python.configs = node_configuration_parameters(python.configs)
        self.assertEqual(python.configs["postgresmainrvers.yml"]["python_port"], "5434")
        self.assertEqual(python.configs["postgresreplicaservers.yml"]["python_port"], "5000")

    @patch("src.database.postgresql.write_to_file")
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_write_to_file):
        postgresql = Postgresql(False)
        postgresql.config_files = ["postgresmainserver.yml"]
        postgresql.configs = {
            "postgresmainserver.yml": {
                "postgresql_version": "12.1"
            }
        }
        postgresql.write_configuration_to_file()
        actual_call = mock_write_to_file.call_args
        expected_call = call('playbooks/group_vars', 'postgresmainserver.yml', postgresql.configs["postgresmainserver.yml"])
        self.assertEqual(actual_call, expected_call)
    