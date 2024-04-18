from src.frameworks.system_framework import SystemFramework
from unittest.mock import MagicMock, patch
import unittest


class TestCustomSelections(unittest.TestCase):
    @patch("src.webservers.python.FileManager.read_from_file")
    def test_init_when_webserver_is_not_none(self, mock_read_from_file):
        user_selections = {
            "webserver": "python",
        } 
        system_framework = SystemFramework(user_selections)
        self.assertIn('webservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    def test_init_when_webserver_is_none(self, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('webservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_database_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "database": "postgresql",
        } 
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework(user_selections) 
        self.assertIn('databasemainserver', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_database_is_none(self, mock_confirm, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('databasemainserver', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_caching_tool_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "caching_tool": "redis",
        } 
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework(user_selections)
        self.assertIn('redisservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_caching_tool_is_none(self, mock_confirm, mock_read_from_file):
        system_framework = SystemFramework({})
        self.assertNotIn('redisservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_is_replica_required_true(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = True
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        self.assertIn('databasereplicaservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    def test_init_when_is_replica_required_false(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        self.assertNotIn('databasereplicaservers', system_framework.selected_host_groups)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.get_hosts_configuration_parameters")
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

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.FileManager.write_to_file")
    def test_apply_configuration_when_it_is_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework({})
        system_framework.environment = "staging"
        system_framework.hosts = {"test": "test"}
        system_framework.apply_configuration()
        self.assertTrue(mock_write_to_file.called)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.FileManager.write_to_file")
    def test_apply_configuration_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        system_framework = SystemFramework({})
        system_framework.database_obj = MagicMock()
        system_framework.webserver_obj = MagicMock()
        system_framework.environment = "staging"
        system_framework.hosts = {"test": "test"}
        system_framework.apply_configuration()
        self.assertEqual(mock_write_to_file.call_count, 2)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    def test_set_configs(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        mock_load_configuration.return_value = {"test": "test"}
        system_framework = SystemFramework({})
        system_framework.webserver_obj = MagicMock()
        system_framework.database_obj = MagicMock()
        system_framework.caching_tool_obj = MagicMock()
        system_framework.set_configs()
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    def test_cset_configs_with_webserver(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selections = {
            "webserver": "python",
        } 
        system_framework = SystemFramework(user_selections)
        system_framework.set_configs()
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    @patch("src.frameworks.system_framework.Python.update_configuration")
    @patch("src.frameworks.system_framework.Postgresql.update_configuration")
    @patch("src.frameworks.system_framework.Redis.update_configuration")
    def test_set_configs_with_database(self, mock_redis_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.set_configs()
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    @patch("src.frameworks.system_framework.Python.update_configuration")
    @patch("src.frameworks.system_framework.Postgresql.update_configuration")
    @patch("src.frameworks.system_framework.Ruby.update_configuration")
    @patch("src.frameworks.system_framework.Redis.update_configuration")
    def test_set_configs_with_database_and_webserver(self, mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
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

    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    @patch("src.frameworks.system_framework.Redis.update_configuration")
    def test_set_configs_with_caching_tool(self, mock_ruby_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "caching_tool": "redis"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.set_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    @patch("src.frameworks.system_framework.Python.update_configuration")
    @patch("src.frameworks.system_framework.Postgresql.update_configuration")
    @patch("src.frameworks.system_framework.Ruby.update_configuration")
    @patch("src.frameworks.system_framework.Redis.update_configuration")
    def test_setup_success(self,mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.side_effect = [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        user_selection = {
            "database": "postgresql",
            "webserver": "ruby",
            "caching_tool": "redis"
        }
        system_framework = SystemFramework(user_selection)
        system_framework.setup()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webservers.python.FileManager.read_from_file")
    @patch("src.frameworks.system_framework.inquirer.confirm")
    @patch("src.frameworks.system_framework.load_configuration")
    @patch("src.frameworks.system_framework.Python.update_configuration")
    @patch("src.frameworks.system_framework.Postgresql.update_configuration")
    @patch("src.frameworks.system_framework.Ruby.update_configuration")
    @patch("src.frameworks.system_framework.Redis.update_configuration")
    def test_setup_failure(self, mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_set_configs = MagicMock(side_effect=Exception("Error setting configs"))
        with patch("src.frameworks.system_framework.SystemFramework.set_configs", mock_set_configs):
            user_selection = {
                "database": "postgresql",
                "webserver": "ruby",
                "caching_tool": "redis"
            }
            system_framework = SystemFramework(user_selection)
            result = system_framework.setup()
            self.assertFalse(result)
            self.assertTrue(mock_set_configs.called)
            self.assertFalse(mock_load_configuration.called)
            self.assertFalse(mock_ruby_parameter_configuration.called)
            self.assertFalse(mock_postgresql_parameter_configuration.called)
            self.assertFalse(mock_redis_parameter_configuration.called)
