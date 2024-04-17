from src.framework.system_framework import SystemFramework
from unittest.mock import MagicMock, patch
import unittest


class TestCustomSelections(unittest.TestCase):
    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_not_none(self, mock_read_from_file):
        user_selections = {
            "webserver": "python",
        } 
        system_framework = SystemFramework(user_selections)
        self.assertIn('webservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_none(self, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('webservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_db_class_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "database": "postgresql",
        } 
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework(user_selections) 
        self.assertIn('databasemainserver', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_db_class_is_none(self, mock_confirm, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('databasemainserver', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_caching_tool_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "caching_tool": "redis",
        } 
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework(user_selections)
        self.assertIn('redisservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_caching_tool_is_none(self, mock_confirm, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('redisservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_replica_server_acceptance_true(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = True
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        self.assertIn('databasereplicaservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    def test_init_when_replica_server_acceptance_false(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        self.assertNotIn('databasereplicaservers', system_framework.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.get_hosts_configuration_parameters")
    def test_set_hosts(self, mock_hosts_configurations_parameters, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework({})
        system_framework.default_hosts = {
            "webservers": {"hosts": {"webserver1": {"ansible_host": "10.10.12.1/23" }}}
        }
        system_framework.set_hosts()
        expected_args = (
            system_framework.selected_host_groups,
            {
                "webservers": {
                    "hosts": {"webserver1": {"ansible_host": "10.10.12.1/23"}}
                }
            },
        )
        mock_hosts_configurations_parameters.assert_called_once_with(*expected_args)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.FileManager.write_to_file")
    def test_apply_configuration_when_it_is_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework({})
        system_framework.environment = "staging"
        system_framework.hosts = {"test": "test"}
        system_framework.apply_configuration()
        self.assertTrue(mock_write_to_file.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.FileManager.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework({})
        system_framework.database_obj = MagicMock()
        system_framework.webserver_obj = MagicMock()
        system_framework.environment = "staging"
        system_framework.hosts = {"test": "test"}
        system_framework.apply_configuration()
        self.assertEqual(mock_write_to_file.call_count, 2)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    def test_check_configs(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        mock_load_configuration.return_value = {"test": "test"}
        system_framework = SystemFramework({})
        system_framework.webserver_obj = MagicMock()
        system_framework.database_obj = MagicMock()
        system_framework.caching_tool_obj = MagicMock()
        system_framework.set_configs()
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    def test_check_configs_with_server_class(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selections = {
            "webserver": "python",
        } 
        system_framework = SystemFramework(user_selections)
        system_framework.set_configs()
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    @patch("src.framework.system_framework.Python.update_configuration")
    @patch("src.framework.system_framework.Postgresql.update_configuration")
    @patch("src.framework.system_framework.Redis.update_configuration")
    def test_check_configs_with_db_class(self, mock_redis_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.set_configs()
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    @patch("src.framework.system_framework.Python.update_configuration")
    @patch("src.framework.system_framework.Postgresql.update_configuration")
    @patch("src.framework.system_framework.Ruby.update_configuration")
    @patch("src.framework.system_framework.Redis.update_configuration")
    def test_check_configs_with_db_and_server_class(self, mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql",
            "webserver": "ruby"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.set_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    @patch("src.framework.system_framework.Redis.update_configuration")
    def test_check_configs_with_additional_service(self, mock_ruby_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "caching_tool": "redis"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.set_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.framework.system_framework.inquirer.confirm")
    @patch("src.framework.system_framework.load_configuration")
    @patch("src.framework.system_framework.Python.update_configuration")
    @patch("src.framework.system_framework.Postgresql.update_configuration")
    @patch("src.framework.system_framework.Ruby.update_configuration")
    @patch("src.framework.system_framework.Redis.update_configuration")
    def test_set_and_execute_configurations(self,mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.side_effect = [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        user_selection = {
            "database": "postgresql",
            "webserver": "ruby",
            "caching_tool": "redis"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.init()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    