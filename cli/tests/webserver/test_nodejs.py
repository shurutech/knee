from src.webserver.nodejs import Nodejs
import unittest
from unittest.mock import patch, call
from src.utils.utils import node_configuration_parameters

class TestNodejs(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        nodejs = Nodejs()
        nodejs.configs = {
            "nodejswebservers.yml": {
                "nodejs_port": "8080"
            }
        }
        with patch("builtins.input", return_value=""):
            nodejs.configs = node_configuration_parameters(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8080")

    def test_parameter_configuration_with_user_input(self):
        nodejs = Nodejs()
        nodejs.configs = {
            "nodejswebservers.yml": {
                "nodejs_port": "8080"
            }
        }
        with patch("builtins.input", return_value="8081"):
            nodejs.configs = node_configuration_parameters(nodejs.configs)
        self.assertEqual(nodejs.configs["nodejswebservers.yml"]["nodejs_port"], "8081")

    @patch("src.webserver.nodejs.write_to_file")
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_write_to_file):
        nodejs = Nodejs()
        nodejs.configs = {
            "nodewebservers.yml": {
                "nodejs_version": "1.21.3"
            }
        }
        nodejs.write_configuration_to_file()
        actual_call = mock_write_to_file.call_args
        expected_call = call('playbooks/group_vars', 'nodewebservers.yml', nodejs.configs["nodewebservers.yml"])
        self.assertEqual(actual_call, expected_call)
    