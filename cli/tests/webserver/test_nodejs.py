from src.webserver.nodejs import Nodejs
import unittest
from unittest.mock import patch, call
from src.utils.utils import load_configuration


class TestNodejs(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        nodejs = Nodejs()
        nodejs.configs = {"nodejswebservers.yml": {"nodejs_port": "8080"}}
        with patch("builtins.input", return_value=""):
            nodejs.configs = load_configuration(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8080")

    def test_parameter_configuration_with_user_input(self):
        nodejs = Nodejs()
        nodejs.configs = {"nodejswebservers.yml": {"nodejs_port": "8080"}}
        with patch("builtins.input", return_value="8081"):
            nodejs.configs = load_configuration(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8081")

    @patch("src.webserver.nodejs.FileManager.write_to_file")
    @patch("src.webserver.nodejs.run_playbook")
    def test_write_configuration_parameters_called_with_expected_arguments(
        self, mock_run_playbook, mock_write_to_file
    ):
        nodejs = Nodejs("local")
        nodejs.configs = {"nodewebservers.yml": {"nodejs_version": "1.21.3"}}
        nodejs.apply_configuration()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "nodewebservers.yml",
            nodejs.configs["nodewebservers.yml"],
        )
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with("node_server.yml", "local")
