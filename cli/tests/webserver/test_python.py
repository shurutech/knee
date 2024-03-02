from cli.src.webserver.python import Python
from cli.src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch

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

    