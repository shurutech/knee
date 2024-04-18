from src.webservers.nodejs import Nodejs
import unittest
from unittest.mock import patch, call
from src.utils.utils import load_configuration


class TestNodejs(unittest.TestCase):
    def test_update_configuration_with_default_values(self):
        nodejs = Nodejs()
        nodejs.configs = {"nodejswebservers.yml": {"nodejs_port": "8080"}}
        with patch("builtins.input", return_value=""):
            nodejs.configs = load_configuration(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8080")

    def test_update_configuration_with_user_input(self):
        nodejs = Nodejs()
        nodejs.configs = {"nodejswebservers.yml": {"nodejs_port": "8080"}}
        with patch("builtins.input", return_value="8081"):
            nodejs.configs = load_configuration(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8081")

    @patch("src.webservers.nodejs.FileManager.write_to_file")
    @patch("src.webservers.nodejs.run_playbook")
    def test_apply_configuration_called_with_expected_arguments(
        self, mock_run_playbook, mock_write_to_file
    ):
        nodejs = Nodejs("local")
        nodejs.configs = {"node_server.yml": {"nodejs_version": "1.21.3"}}
        nodejs.apply_configuration()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "node_server.yml",
            nodejs.configs["node_server.yml"],
        )
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with("node_server.yml", "local")
