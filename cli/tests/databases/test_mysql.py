import unittest
from unittest.mock import patch
from src.databases.mysql import Mysql


class TestMysql(unittest.TestCase):
    @patch("src.databases.mysql.FileManager.read_from_file")
    def test_initialiser_with_file(self, mock_read_from_file):
        mock_read_from_file.return_value = {
            "mysql_server.yml": {"mysql_port": "3307"}
        }
        mysql = Mysql()
        self.assertEqual(
            mysql.configs["mysql_server.yml"]["mysql_server.yml"]["mysql_port"],
            "3307",
        )

    @patch("src.databases.mysql.load_configuration")
    def test_update_configuration(self, mock_load_configuration):
        mysql = Mysql()
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"}
        }
        mock_load_configuration.return_value = {
            "mysql_server.yml": {"mysql_port": "3307"}
        }
        mysql.update_configuration()
        mock_load_configuration.assert_called_once_with( {
            "mysql_server.yml": {"mysql_port": "3305"}
        })
        self.assertEqual(
              mysql.configs["mysql_server.yml"]["mysql_port"],
              "3307",
         )

    @patch("src.databases.mysql.load_configuration")
    def test_update_configuration_raises_error(self, mock_load_configuration):
        mysql = Mysql()
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"}
        }
        mock_load_configuration.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            mysql.update_configuration()
        self.assertTrue('Error' in str(context.exception))

    @patch("src.databases.mysql.FileManager.write_to_file")
    @patch("src.databases.mysql.run_playbook")
    def test_apply_configuration(self, mock_run_playbook, mock_write_to_file):
        mysql = Mysql()
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"}
        }
        mysql.apply_configuration()
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "mysql_server.yml", {"mysql_port": "3305"}
        )
        mock_run_playbook.assert_called_once_with("mysql_server.yml", "local")

    @patch("src.databases.mysql.FileManager.write_to_file")
    @patch("src.databases.mysql.run_playbook")
    def test_apply_configuration_when_write_to_file_raises_error(self, mock_run_playbook, mock_write_to_file):
        mysql = Mysql()
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"}
        }
        mock_write_to_file.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            mysql.apply_configuration()
        self.assertTrue('Error' in str(context.exception))
        mock_run_playbook.assert_not_called()
    
    @patch("src.databases.mysql.FileManager.write_to_file")
    @patch("src.databases.mysql.run_playbook")
    def test_apply_configuration_when_run_playbook_raises_error(self, mock_run_playbook, mock_write_to_file):
        mysql = Mysql()
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"}
        }
        mock_run_playbook.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            mysql.apply_configuration()
        self.assertTrue('Error' in str(context.exception))
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "mysql_server.yml", {"mysql_port": "3305"}
        )

    @patch("src.databases.mysql.FileManager.write_to_file")
    @patch("src.databases.mysql.run_playbook")
    def test_apply_configuration_when_is_replica_required_is_true(self, mock_run_playbook, mock_write_to_file):
        mysql = Mysql()
        mysql.is_replica_required = True
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"},
            "mysql_replica_server.yml": {"mysql_port": "3306"}
        }
        mysql.apply_configuration()
        if mysql.is_replica_required:
            mock_run_playbook.assert_called_once_with("mysql_replica_server.yml", "local")

    @patch("src.databases.mysql.FileManager.write_to_file")
    @patch("src.databases.mysql.run_playbook")
    def test_apply_configuration_when_is_replica_required_is_false(self, mock_run_playbook, mock_write_to_file):
        mysql = Mysql()
        mysql.is_replica_required = False
        mysql.configs = {
            "mysql_server.yml": {"mysql_port": "3305"},
        }
        mysql.apply_configuration()
        if not mysql.is_replica_required:
            mock_run_playbook.assert_called_once_with("mysql_server.yml", "local")
