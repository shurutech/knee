from src.webserver.python import Python
from src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch, call

class TestPython(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        python = Python()
        python.configs = {
            "pythonwebservers.yml": {
                "python_port": "5432"
            }
        }
        with patch("builtins.input", return_value=""):
            python.configs = node_configuration_parameters(python.configs)
        self.assertEqual(python.configs["pythonwebservers.yml"]["python_port"], "5432")

    def test_parameter_configuration_with_user_input(self):
        python = Python()
        python.configs = {
            "pythonwebservers.yml": {
                "python_port": "5432"
            }
        }
        with patch("builtins.input", return_value="5434"):
            python.configs = node_configuration_parameters(python.configs)
        self.assertEqual(python.configs["pythonwebservers.yml"]["python_port"], "5434")

    @patch("src.webserver.python.write_to_file")
    def test_write_configuration_parameters_called_with_expected_arguments(self, mock_write_to_file):
        python = Python()
        Python.configs = {
            "pythonwebservers.yml": {
                "python_version": "3.8.1"
            }
        }
        python.write_configuration_to_file()
        actual_call = mock_write_to_file.call_args
        expected_call = call('playbooks/group_vars', 'pythonwebservers.yml', {'python_version': Python.configs["pythonwebservers.yml"]["python_version"]})
        self.assertEqual(actual_call, expected_call)

    