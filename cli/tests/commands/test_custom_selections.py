from src.commands.custom_system import CustomSystem
from unittest.mock import MagicMock, patch
import unittest


class TestCustomSelections(unittest.TestCase):
    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_not_none(self, mock_read_from_file):
        user_selections = {
            "webserver": "python",
        } 
        custom_system = CustomSystem(user_selections)
        self.assertIn('webservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    def test_init_when_server_class_is_none(self, mock_read_from_file):
        custom_system = CustomSystem({})
        self.assertNotIn('webservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_db_class_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "database": "postgresql",
        } 
        mock_confirm.return_value.execute.return_value = False
        custom_system = CustomSystem(user_selections) 
        self.assertIn('databasemainserver', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_db_class_is_none(self, mock_confirm, mock_read_from_file):
        custom_system = CustomSystem({})
        self.assertNotIn('databasemainserver', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_caching_tool_is_not_none(self, mock_confirm, mock_read_from_file):
        user_selections = {
            "caching_tool": "redis",
        } 
        mock_confirm.return_value.execute.return_value = False
        custom_system = CustomSystem(user_selections)
        self.assertIn('redisservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_caching_tool_is_none(self, mock_confirm, mock_read_from_file):
        custom_system = CustomSystem({})
        self.assertNotIn('redisservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_replica_server_acceptance_true(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = True
        user_selection = {
            "database": "postgresql"
        }
        custom_system = CustomSystem(user_selection)
        self.assertIn('databasereplicaservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    def test_init_when_replica_server_acceptance_false(self, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        custom_system = CustomSystem(user_selection)
        self.assertNotIn('databasereplicaservers', custom_system.selected_host_groups)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.get_hosts_configuration_parameters")
    def test_set_hosts(self, mock_hosts_configurations_parameters, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_system = CustomSystem({})
        custom_system.default_hosts = {
            "webservers": {"hosts": {"webserver1": {"ansible_host": "10.10.12.1/23" }}}
        }
        custom_system.set_hosts()
        expected_args = (
            custom_system.selected_host_groups,
            {
                "webservers": {
                    "hosts": {"webserver1": {"ansible_host": "10.10.12.1/23"}}
                }
            },
        )
        mock_hosts_configurations_parameters.assert_called_once_with(*expected_args)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.FileManager.write_to_file")
    def test_apply_configuration_when_it_is_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_system = CustomSystem({})
        custom_system.environment = "staging"
        custom_system.hosts = {"test": "test"}
        custom_system.apply_configuration()
        self.assertTrue(mock_write_to_file.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.FileManager.write_to_file")
    def test_number_of_times_write_to_file_called(self, mock_write_to_file, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        custom_system = CustomSystem({})
        custom_system.database_obj = MagicMock()
        custom_system.webserver_obj = MagicMock()
        custom_system.environment = "staging"
        custom_system.hosts = {"test": "test"}
        custom_system.apply_configuration()
        self.assertEqual(mock_write_to_file.call_count, 2)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    def test_check_configs(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        mock_load_configuration.return_value = {"test": "test"}
        custom_system = CustomSystem({})
        custom_system.webserver_obj = MagicMock()
        custom_system.database_obj = MagicMock()
        custom_system.caching_tool_obj = MagicMock()
        custom_system.set_configs()
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    def test_check_configs_with_server_class(self, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selections = {
            "webserver": "python",
        } 
        custom_system = CustomSystem(user_selections)
        custom_system.set_configs()
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    @patch("src.commands.custom_system.Python.update_configuration")
    @patch("src.commands.custom_system.Postgresql.update_configuration")
    @patch("src.commands.custom_system.Redis.update_configuration")
    def test_check_configs_with_db_class(self, mock_redis_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql"
        }
        custom_system = CustomSystem(user_selection)
        custom_system.set_configs()
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    @patch("src.commands.custom_system.Python.update_configuration")
    @patch("src.commands.custom_system.Postgresql.update_configuration")
    @patch("src.commands.custom_system.Ruby.update_configuration")
    @patch("src.commands.custom_system.Redis.update_configuration")
    def test_check_configs_with_db_and_server_class(self, mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "database": "postgresql",
            "webserver": "ruby"
        }
        custom_system = CustomSystem(user_selection)
        custom_system.set_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)

    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    @patch("src.commands.custom_system.Redis.update_configuration")
    def test_check_configs_with_additional_service(self, mock_ruby_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.return_value.execute.return_value = False
        user_selection = {
            "caching_tool": "redis"
        }
        custom_system = CustomSystem(user_selection)
        custom_system.set_configs()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)
    
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.commands.custom_system.inquirer.confirm")
    @patch("src.commands.custom_system.load_configuration")
    @patch("src.commands.custom_system.Python.update_configuration")
    @patch("src.commands.custom_system.Postgresql.update_configuration")
    @patch("src.commands.custom_system.Ruby.update_configuration")
    @patch("src.commands.custom_system.Redis.update_configuration")
    def test_set_and_execute_configurations(self,mock_redis_parameter_configuration, mock_ruby_parameter_configuration, mock_postgresql_parameter_configuration, mock_python_parameter_configuration, mock_load_configuration, mock_confirm, mock_read_from_file):
        mock_confirm.side_effect = [MagicMock(execute=lambda: False), MagicMock(execute=lambda: False)]
        user_selection = {
            "database": "postgresql",
            "webserver": "ruby",
            "caching_tool": "redis"
        }
        custom_system = CustomSystem(user_selection)
        custom_system.init()
        self.assertTrue(mock_ruby_parameter_configuration.called)
        self.assertTrue(mock_postgresql_parameter_configuration.called)
        self.assertTrue(mock_load_configuration.called)






    

    

        
        