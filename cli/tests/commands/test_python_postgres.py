from src.commands.python_postgres import PythonPostgres
import unittest
from unittest.mock import patch
class TestPythonPostgres(unittest.TestCase) : 
    # def test_check_defaults(self):
    #     pp = Postgresql()
    #     assert True

    @patch('python_postgres.inquirer.confirm')
    @patch('python_postgres.read_from_file')
    @patch('python_postgres.Python.__init__')
    @patch('python_postgres.Postgresql.__init__')
    def test_init(self, mock_postgresql_init, mock_python_init, mock_read_from_file, mock_confirm):
        mock_read_from_file.return_value = {}
        mock_confirm.return_value.execute.return_value = True
        pp = PythonPostgres()
        mock_confirm.assert_called_with(message="Do you want to setup a replica server? (Default= No) :: ", default=False)
        self.assertIn("databasereplicaservers", pp.IMPACTED_HOST_GROUPS)

        mock_read_from_file.assert_any_call('playbooks/group_vars', 'all.yml')
        mock_read_from_file.assert_any_call('playbooks/group_vars', 'webservers.yml')

        mock_python_init.assert_called_once()
        mock_postgresql_init.assert_called_once_with(False)
