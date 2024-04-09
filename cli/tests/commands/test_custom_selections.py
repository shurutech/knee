from src.commands.custom_selections import CustomSelections
from unittest.mock import MagicMock, patch
import unittest


class TestCustomSelections(unittest.TestCase):
    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_not_none(self, mock_read_from_file):
        server_class = "python"
        custom_selections = CustomSelections(server_class=server_class)
        self.assertIn('webservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_none(self, mock_read_from_file):
        custom_selections = CustomSelections()
        self.assertNotIn('webservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_db_class_is_not_none(self, mock_confirm, mock_read_from_file):
        db_client_class = "postgresql"
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(db_client_class=db_client_class) 
        self.assertIn('databasemainserver', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_db_class_is_none(self, mock_confirm, mock_read_from_file):
        custom_selections = CustomSelections()
        self.assertNotIn('databasemainserver', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_additional_service_is_not_none(self, mock_confirm, mock_read_from_file):
        additional_service = "redis"
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(additional_service=additional_service)
        self.assertIn('redisservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_additional_service_is_none(self, mock_confirm, mock_read_from_file):
        custom_selections = CustomSelections()
        self.assertNotIn('redisservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_replica_server_acceptance_true(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = True
        custom_selections = CustomSelections(db_client_class="postgresql")
        self.assertIn('databasereplicaservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    def test_init_when_replica_server_acceptance_false(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(db_client_class="postgresql")
        self.assertNotIn('databasereplicaservers', custom_selections.impacted_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.hosts_configuration_parameters")
    def test_check_hosts(self, mock_hosts_configurations_parameters, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections()
        custom_selections.hosts = {
            "webservers": {"hosts": {"webserver1": {"ansible_host": "10.10.12.1/23" }}}
        }
        custom_selections.check_hosts()
        expected_args = (
            custom_selections.impacted_host_groups,
            {
                "webservers": {
                    "hosts": {"webserver1": {"ansible_host": "10.10.12.1/23"}}
                }
            },
        )
        mock_hosts_configurations_parameters.assert_called_once_with(*expected_args)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.FileManager.write_to_file")
    def test_write_configuration_and_run_playbook_when_it_is_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections()
        custom_selections.environment = "staging"
        custom_selections.hosts = {"test": "test"}
        custom_selections.apply_configuration()
        self.assertTrue(mock_write_to_file.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.FileManager.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections()
        custom_selections.database = MagicMock()
        custom_selections.server = MagicMock()
        custom_selections.environment = "staging"
        custom_selections.hosts = {"test": "test"}
        custom_selections.apply_configuration()
        self.assertEqual(mock_write_to_file.call_count, 2)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    def test_check_configs(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        mock_load_configuration.return_value = {"test": "test"}
        custom_selections = CustomSelections()
        custom_selections.server = MagicMock()
        custom_selections.database = MagicMock()
        custom_selections.additional_service = MagicMock()
        custom_selections.check_configs()
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    def test_check_configs_with_server_class(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(server_class="python")
        custom_selections.check_configs()
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    @patch("src.commands.custom_selections.Python.parameter_configuration")
    @patch("src.commands.custom_selections.Postgresql.parameter_configuration")
    @patch("src.commands.custom_selections.Redis.parameter_configuration")
    def test_check_configs_with_db_class(self, mock_redis_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(db_client_class="postgresql")
        custom_selections.check_configs()
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    @patch("src.commands.custom_selections.Python.parameter_configuration")
    @patch("src.commands.custom_selections.Postgresql.parameter_configuration")
    @patch("src.commands.custom_selections.Ruby.parameter_configuration")
    @patch("src.commands.custom_selections.Redis.parameter_configuration")
    def test_check_configs_with_db_and_server_class(self, mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(db_client_class="postgresql", server_class="ruby")
        custom_selections.check_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    @patch("src.commands.custom_selections.Redis.parameter_configuration")
    def test_check_configs_with_additional_service(self, mock_ruby_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_selections = CustomSelections(additional_service="redis")
        custom_selections.check_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_selections.inquirer.confirm")
    @patch("src.commands.custom_selections.load_configuration")
    @patch("src.commands.custom_selections.Python.parameter_configuration")
    @patch("src.commands.custom_selections.Postgresql.parameter_configuration")
    @patch("src.commands.custom_selections.Ruby.parameter_configuration")
    @patch("src.commands.custom_selections.Redis.parameter_configuration")
    def test_check_defaults(self,mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.side_effect = [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        custom_selections = CustomSelections(db_client_class="postgresql", server_class="ruby", additional_service="redis")
        custom_selections.check_defaults()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)






    

    

        
        