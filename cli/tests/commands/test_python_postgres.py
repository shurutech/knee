from src.commands.python_postgres import PythonPostgres, IMPACTED_HOST_GROUPS, CONFIG_FILES
import unittest
from unittest.mock import patch, call, MagicMock
class TestPythonPostgres(unittest.TestCase) : 
    @patch("src.commands.python_postgres.inquirer.confirm")
    def test_init_with_replica_server_acceptance_true(self, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = True
        PythonPostgres()
        assert "databasereplicaservers" in IMPACTED_HOST_GROUPS
    
    @patch("src.commands.python_postgres.inquirer.confirm")
    def test_init_with_replica_server_acceptance_false(self, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = False
        PythonPostgres()
        assert "databasereplicaservers" not in IMPACTED_HOST_GROUPS

    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch("src.commands.python_postgres.hosts_configuration_parameters")
    def test_check_hosts(self, mock_hosts_configurations_parameters, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = False
        python_postgres = PythonPostgres()
        python_postgres.hosts = {
            "webservers": {
                "hosts": {
                    "webserver1": {
                        "ansible_host": "10.10.10.1/23"
                    }
                }
            }
        }
        python_postgres.check_hosts()
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

    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch.object(PythonPostgres, "write_configuration_and_run_playbook")
    def test_write_configuration_and_run_playbook_when_it_is_called(self, mock_write_to_file, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = False
        python_postgres = PythonPostgres()
        python_postgres.environment = "staging"
        python_postgres.hosts = {"test": "test"}
        python_postgres.write_configuration_and_run_playbook()
        assert mock_write_to_file.called
    
    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch("src.commands.python_postgres.FileManager.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = False
        python_postgres = PythonPostgres()
        python_postgres.database = MagicMock()
        python_postgres.server = MagicMock()
        python_postgres.environment = "staging"
        python_postgres.hosts = {"test": "test"}
        python_postgres.write_configuration_and_run_playbook()
        assert mock_write_to_file.call_count == 1 + CONFIG_FILES.__len__()  

    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch("src.commands.python_postgres.PythonPostgres.check_configs")
    @patch("src.commands.python_postgres.PythonPostgres.check_hosts")
    @patch("src.commands.python_postgres.PythonPostgres.write_configuration_and_run_playbook")
    def test_check_defaults_with_configuration_when_acceptance_is_true(self, mock_write_configuration_and_run_playbook ,mock_check_hosts, mock_check_configs, mock_confirm) : 
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: True)]
        python_postgres = PythonPostgres()
        python_postgres.check_defaults()
        assert mock_check_configs.called
        assert mock_check_hosts.called
        assert mock_write_configuration_and_run_playbook.called

    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch("src.commands.python_postgres.load_configuration")
    @patch("src.commands.python_postgres.Python.parameter_configuration")
    @patch("src.commands.python_postgres.Postgresql.parameter_configuration")
    def test_check_configs(self, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm) : 
        mock_confirm.return_value.execute.return_value = False
        python_postgres = PythonPostgres()
        python_postgres.check_configs()
        assert mock_python_parameter_configuration.called
        assert mock_postgresql_parameter_configuration.called
        assert mock_load_configuration.called

    @patch("src.commands.python_postgres.inquirer.confirm")
    @patch("src.commands.python_postgres.PythonPostgres.check_configs")
    @patch("src.commands.python_postgres.PythonPostgres.check_hosts")
    @patch("src.commands.python_postgres.PythonPostgres.write_configuration_and_run_playbook")
    def test_check_defaults_with_configuration_when_acceptance_is_false(self, mock_write_configuration_and_run_playbook ,mock_check_hosts, mock_check_configs, mock_confirm) : 
        mock_confirm.side_effect =  [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        python_postgres = PythonPostgres()
        python_postgres.check_defaults()
        assert mock_check_configs.called
        assert mock_check_hosts.called
        assert not mock_write_configuration_and_run_playbook.called
