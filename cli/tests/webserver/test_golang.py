from cli.src.webserver.golang import Golang
import unittest
from unittest.mock import patch
from cli.src.utils.utils import node_configuration_parameters

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