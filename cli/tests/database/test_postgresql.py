from cli.src.database.postgresql import Postgresql
from cli.src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch
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
    