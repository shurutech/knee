from src.webserver.nodejs import Nodejs
import unittest
from unittest.mock import patch
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
    