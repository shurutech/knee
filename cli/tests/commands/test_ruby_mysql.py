from src.commands.ruby_mysql import RubyMysql, IMPACTED_HOST_GROUPS, CONFIG_FILES
import unittest
from unittest.mock import patch, MagicMock

class TestRubyMysql(unittest.TestCase) :

    @patch("src.commands.ruby_mysql.inquirer.confirm")
    def test_init_with_replica_server_acceptance_true(self, mock_confirm) :
        mock_confirm.return_value.execute.return_value = True
        RubyMysql()
        assert "databasereplicaservers" in IMPACTED_HOST_GROUPS
    
    @patch("src.commands.ruby_mysql.inquirer.confirm")
    def test_init_with_replica_server_acceptance_false(self, mock_confirm) :
        mock_confirm.return_value.execute.return_value = False
        RubyMysql()
        assert "databasereplicaservers" not in IMPACTED_HOST_GROUPS

    @patch("src.commands.ruby_mysql.inquirer.confirm")
    @patch("src.commands.ruby_mysql.hosts_configuration_parameters")
    def test_check_hosts(self, mock_hosts_configurations_parameters, mock_confirm) :
        mock_confirm.return_value.execute.return_value = False
        ruby_mysql = RubyMysql()
        ruby_mysql.hosts = {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.10.1/23"
                    }
                }
            }
        }
        ruby_mysql.check_hosts()
        expected_args = (IMPACTED_HOST_GROUPS,  {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.10.1/23"
                    }
                }
            }
        })
        mock_hosts_configurations_parameters.assert_called_once_with(*expected_args)
    
    @patch("src.commands.ruby_mysql.inquirer.confirm")
    @patch.object(RubyMysql, "write_configuration_and_run_playbook")
    def test_write_configuration_and_run_playbook_when_it_is_called(self, mock_write_to_file, mock_confirm) :
        mock_confirm.return_value.execute.return_value = False
        ruby_mysql = RubyMysql()
        ruby_mysql.environment = "staging"
        ruby_mysql.hosts = {"test": "test"}
        ruby_mysql.write_configuration_and_run_playbook()
        assert mock_write_to_file.called

    @patch("src.commands.ruby_mysql.inquirer.confirm")
    @patch("src.commands.ruby_mysql.FileManager.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm) :
        mock_confirm.return_value.execute.return_value = False
        ruby_mysql = RubyMysql()
        ruby_mysql.database = MagicMock()
        ruby_mysql.server = MagicMock()
        ruby_mysql.environment = "staging"
        ruby_mysql.hosts = {"test": "test"}
        ruby_mysql.write_configuration_and_run_playbook()
        assert mock_write_to_file.call_count == 1 + CONFIG_FILES.__len__()
