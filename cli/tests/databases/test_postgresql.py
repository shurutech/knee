from src.databases.postgresql import Postgresql
from src.utils.utils import load_configuration
import unittest
from unittest.mock import patch, call


class TestPostgresql(unittest.TestCase):
    def test_update_configuration_with_default_values(self):
        postgresql = Postgresql()
        postgresql.configs = {"mainserver.yml": {"postgresql_port": "5432"}}
        with patch("builtins.input", return_value=""):
            postgresql.configs = load_configuration(postgresql.configs)
        self.assertEqual(
            postgresql.configs["mainserver.yml"]["postgresql_port"], "5432"
        )

    def test_update_configuration_with_user_input(self):
        postgresql = Postgresql()
        postgresql.configs = {"mainserver.yml": {"postgresql_port": "5432"}}
        with patch("builtins.input", return_value="5434"):
            postgresql.configs = load_configuration(postgresql.configs)
        self.assertEqual(
            postgresql.configs["mainserver.yml"]["postgresql_port"], "5434"
        )

    def test_update_configuration_when_is_replica_required_acceptance(self):
        python = Postgresql(True)
        python.configs = {
            "postgresmainrvers.yml": {"python_port": "5432"},
            "postgres_replica_server.yml": {"python_port": "5432"},
        }
        with patch("builtins.input", side_effect=["5434", "5000"]):
            python.configs = load_configuration(python.configs)
        self.assertEqual(python.configs["postgresmainrvers.yml"]["python_port"], "5434")
        self.assertEqual(
            python.configs["postgres_replica_server.yml"]["python_port"], "5000"
        )

    @patch("src.databases.postgresql.FileManager.write_to_file")
    @patch("src.databases.postgresql.run_playbook")
    def test_apply_configuration_called_with_expected_arguments(
        self, mock_run_playbook, mock_write_to_file
    ):
        postgresql = Postgresql(False, "staging")
        postgresql.config_files = ["postgres_server.yml"]
        postgresql.configs = {"postgres_server.yml": {"postgresql_version": "12.1"}}
        postgresql.apply_configuration()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "postgres_server.yml",
            postgresql.configs["postgres_server.yml"],
        )
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with("postgres_server.yml", "staging")
