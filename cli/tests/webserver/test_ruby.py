from src.webserver.ruby import Ruby
from src.utils.utils import node_configuration_parameters
import unittest
from unittest.mock import patch

class TestRuby(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        ruby = Ruby()
        ruby.configs = {
            "rubywebservers.yml": {
                "ruby_port": "8080"
            }
        }
        with patch("builtins.input", return_value=""):
            ruby.configs = node_configuration_parameters(ruby.configs)
        self.assertEqual(ruby.configs["rubywebservers.yml"]["ruby_port"], "8080")

    def test_parameter_configuration_with_user_input(self):
        ruby = Ruby()
        ruby.configs = {
            "rubywebservers.yml": {
                "ruby_port": "8080"
            }
        }
        with patch("builtins.input", return_value="8081"):
            ruby.configs = node_configuration_parameters(ruby.configs)
        self.assertEqual(ruby.configs["rubywebservers.yml"]["ruby_port"], "8081")