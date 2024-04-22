from src.webservers.ruby import Ruby
import unittest
from unittest.mock import patch


class TestRuby(unittest.TestCase):
    @patch("src.webservers.ruby.FileManager.read_from_file")
    def test_initialiser_with_file(self, mock_read_from_file):
        mock_read_from_file.return_value = {
            "ruby_port": "3307"
        }
        ruby = Ruby()
        self.assertEqual(
            ruby.configs["ruby_webserver.yml"]["ruby_port"],
            "3307",
        )

    @patch("src.webservers.ruby.load_configuration")
    def test_update_configuration(self, mock_load_configuration):
        ruby = Ruby()
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_load_configuration.return_value = {
            "rubyserver.yml": {"ruby_port": "3307"}
        }
        ruby.update_configuration()
        mock_load_configuration.assert_called_once_with( {
            "rubyserver.yml": {"ruby_port": "3305"}
        })
        self.assertEqual(
              ruby.configs["rubyserver.yml"]["ruby_port"],
              "3307",
         )

    @patch("src.webservers.ruby.load_configuration")
    def test_update_configuration_raises_error(self, mock_load_configuration):
        ruby = Ruby()
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_load_configuration.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.update_configuration()
        self.assertTrue('Error' in str(context.exception))

    @patch("src.webservers.ruby.FileManager.write_to_file")
    @patch("src.webservers.ruby.run_playbook")
    def test_apply_configuration(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
             "rubyserver.yml": {"ruby_port": "3305"}
        }
        ruby.apply_configuration()
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "rubyserver.yml", {"ruby_port": "3305"}
        )
        mock_run_playbook.assert_any_call("webserver_base.yml", "local")
        mock_run_playbook.assert_any_call("ruby_webserver.yml", "local")
        assert mock_run_playbook.call_count == 2

    @patch("src.webservers.ruby.FileManager.write_to_file")
    @patch("src.webservers.ruby.run_playbook")
    def test_apply_configuration_when_write_to_file_raises_error(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_write_to_file.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.apply_configuration()
        self.assertTrue('Error' in str(context.exception))  
        mock_run_playbook.assert_not_called()

    @patch("src.webservers.ruby.FileManager.write_to_file")
    @patch("src.webservers.ruby.run_playbook")
    def test_apply_configuration_when_run_playbook_raises_error(self, mock_run_playbook, mock_write_to_file):
        ruby = Ruby()
        ruby.CONFIG_FILES = ["rubyserver.yml"]
        ruby.configs = {
            "rubyserver.yml": {"ruby_port": "3305"}
        }
        mock_run_playbook.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            ruby.apply_configuration()
        self.assertTrue('Error' in str(context.exception))  
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "rubyserver.yml", {"ruby_port": "3305"}
        )
        