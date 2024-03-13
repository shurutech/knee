from src.webserver.golang import Golang
import unittest
from unittest.mock import patch, call
from src.utils.utils import node_configuration_parameters

class TestGolang(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        golang = Golang()
        golang.configs = {
            "golangwebservers.yml": {
                "golang_port": "8080"
            }
        }
        with patch("builtins.input", return_value=""):
            golang.configs = node_configuration_parameters(golang.configs)
        self.assertEqual(golang.configs["golangwebservers.yml"]["golang_port"], "8080")

    def test_parameter_configuration_with_user_input(self):
        golang = Golang()
        golang.configs = {
            "golangwebservers.yml": {
                "golang_port": "8080"
            }
        }
        with patch("builtins.input", return_value="8081"):
            golang.configs = node_configuration_parameters(golang.configs)
        self.assertEqual(golang.configs["golangwebservers.yml"]["golang_port"], "8081")
    
    @patch("src.webserver.golang.write_to_file")
    @patch("src.webserver.golang.run_playbook")
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_run_playbook, mock_write_to_file):
        golang = Golang('local')
        Golang.configs = {
            "golangwebservers.yml": {
                "golang_version": "1.21.3"
            }
        }
        golang.write_configuration_and_run_playbook()
        actual_call = mock_write_to_file.call_args
        expected_call = call('playbooks/group_vars', 'golangwebservers.yml', {'golang_version': Golang.configs["golangwebservers.yml"]["golang_version"]})
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with('golang_server.yml', 'local')
        