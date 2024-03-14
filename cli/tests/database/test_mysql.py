from src.database.mysql import Mysql
from src.utils.utils import load_configuration
import unittest
from unittest.mock import patch


class TestMysql(unittest.TestCase):
    def test_parameter_configuration_with_default_values(self):
        mysql = Mysql()
        mysql.configs = {"mysqlmainserver.yml": {"mysql_port": "3306"}}
        with patch("builtins.input", return_value=""):
            mysql.configs = load_configuration(mysql.configs)
        self.assertEqual(mysql.configs["mysqlmainserver.yml"]["mysql_port"], "3306")

    def test_parameter_configuration_with_user_input(self):
        mysql = Mysql()
        mysql.configs = {"mysqlmainserver.yml": {"mysql_port": "3306"}}
        with patch("builtins.input", return_value="3307"):
            mysql.configs = load_configuration(mysql.configs)
        self.assertEqual(mysql.configs["mysqlmainserver.yml"]["mysql_port"], "3307")

    def test_parameter_configuration_with_replica_server_acceptance(self):
        mysql = Mysql(True)
        mysql.configs = {
            "mysqlwebservers.yml": {"mysql_port": "3306"},
            "mysqlreplicaservers.yml": {"mysql_port": "3306"},
        }
        with patch("builtins.input", side_effect=["3307", "3308"]):
            mysql.configs = load_configuration(mysql.configs)
        self.assertEqual(mysql.configs["mysqlwebservers.yml"]["mysql_port"], "3307")
        self.assertEqual(mysql.configs["mysqlreplicaservers.yml"]["mysql_port"], "3308")
