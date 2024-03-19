from src.webserver.ruby import Ruby
from src.utils.utils import load_configuration
import unittest
from unittest.mock import patch


class TestRuby(unittest.TestCase):
    @patch("src.webserver.ruby.FileManager.read_from_file")
    def test_initialiser_with_file(self, mock_read_from_file):
        mock_read_from_file.return_value = {
            "ruby_port": "3307"
        }
        ruby = Ruby()
        self.assertEqual(
            ruby.configs["rubywebservers.yml"]["ruby_port"],
            "3307",
        )

    @patch("src.webserver.ruby.load_configuration")
    def test_parameter_configuration(self, mock_load_configuration):
        ruby = Ruby()
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_load_configuration.return_value = {
            "rubyserver.yml": {"ruby_port": "3307"}
        }
        ruby.parameter_configuration()
        mock_load_configuration.assert_called_once_with( {
            "rubyserver.yml": {"ruby_port": "3305"}
        })
        self.assertEqual(
              ruby.configs["rubyserver.yml"]["ruby_port"],
              "3307",
         )

    @patch("src.webserver.ruby.load_configuration")
    def test_parameter_configuration_raises_error(self, mock_load_configuration):
        ruby = Ruby()
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_load_configuration.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.parameter_configuration()
        self.assertTrue('Error' in str(context.exception))

    @patch("src.webserver.ruby.FileManager.write_to_file")
    @patch("src.webserver.ruby.run_playbook")
    def test_write_configuration_and_run_playbook(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
             "rubyserver.yml": {"ruby_port": "3305"}
        }
        ruby.write_configuration_and_run_playbook()
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "rubyserver.yml", {"ruby_port": "3305"}
        )
        mock_run_playbook.assert_any_call("webserver_base.yml", "local")
        mock_run_playbook.assert_any_call("ruby_webservers.yml", "local")
        assert mock_run_playbook.call_count == 2

    @patch("src.webserver.ruby.FileManager.write_to_file")
    @patch("src.webserver.ruby.run_playbook")
    def test_write_configuration_and_run_playbook_when_write_to_file_raises_error(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_write_to_file.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.write_configuration_and_run_playbook()
        self.assertTrue('Error' in str(context.exception))  
        mock_run_playbook.assert_not_called()

    @patch("src.webserver.ruby.FileManager.write_to_file")
    @patch("src.webserver.ruby.run_playbook")
    def test_write_configuration_and_run_playbook_when_run_playbook_raises_error(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_run_playbook.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.write_configuration_and_run_playbook()
        self.assertTrue('Error' in str(context.exception))  
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "rubyserver.yml", {"ruby_port": "3305"}
        )
        