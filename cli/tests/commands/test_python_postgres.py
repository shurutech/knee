import pytest
import os
import yaml
from cli.src.commands.python_postgres import PythonPostgres
import tempfile
from cli.src.commands.python_postgres import get_user_input, get_user_confirmation, write_to_file
from unittest.mock import patch, mock_open, call
import unittest


# class TestPythonPostgres:
#     def test_check_hosts_raise_argument_error_if_default_ip(self):
#         pp = PythonPostgres(environment="local")
#         with pytest.raises(ValueError) as message:
#             pp.check_hosts()
#         assert (
#             "Host: webserver1, Ansible Host: 192.168.181.128 is set to default IP. Please set the ansible_host for the host."
#             in str(message.value)
#         )

#     def test_check_hosts_does_not_raise_argument_error_if_not_default_ip(self):
#         pp = PythonPostgres(environment="local")
#         response = pp.check_hosts(default_ip="10.10.10.10")
#         assert response is True

#     @patch("cli.src.commands.python_postgres.IMPACTED_HOST_GROUPS")
#     @patch("cli.src.commands.python_postgres.yaml.safe_load")
#     def test_check_hosts_default_ip_present_in_non_impacted_host_group(
#         self, mock_safe_load, mock_impacted_host_groups
#     ):
#         pp = PythonPostgres(environment="local")
#         mock_data = {
#             "postgresmainserver": {
#                 "hosts": {
#                     "mainserver": {
#                         "ansible_connection": "ssh",
#                         "ansible_host": "192.168.181.128",
#                         "ansible_port": 22,
#                         "ansible_ssh_private_key_file": ".vagrant/machines/vm1/vmware_fusion/private_key",
#                         "ansible_user": "vagrant",
#                     }
#                 }
#             },
#             "postgresreplicaservers": {
#                 "hosts": {
#                     "replica1": {
#                         "ansible_connection": "ssh",
#                         "ansible_host": "192.168.181.129",
#                         "ansible_port": 22,
#                         "ansible_ssh_private_key_file": ".vagrant/machines/vm2/vmware_fusion/private_key",
#                         "ansible_user": "vagrant",
#                     }
#                 }
#             },
#         }
#         mock_safe_load.return_value = mock_data
#         mock_impacted_host_groups.return_value = [
#             "pythonwebservers",
#             "postgresmainserver",
#         ]

#         response = pp.check_hosts(default_ip="192.168.181.128")
#         assert response is True

#     @patch("cli.src.commands.python_postgres.IMPACTED_HOST_GROUPS")
#     @patch("cli.src.commands.python_postgres.yaml.safe_load")
#     def test_check_hosts_not_default_ip_and_non_impacted_host_group(
#         self, mock_safe_load, mock_impacted_host_groups
#     ):
#         pp = PythonPostgres(environment="local")
#         mock_data = {
#             "postgresmainserver": {
#                 "hosts": {
#                     "mainserver": {
#                         "ansible_connection": "ssh",
#                         "ansible_host": "192.168.181.128",
#                         "ansible_port": 22,
#                         "ansible_ssh_private_key_file": ".vagrant/machines/vm1/vmware_fusion/private_key",
#                         "ansible_user": "vagrant",
#                     }
#                 }
#             },
#             "postgresreplicaservers": {
#                 "hosts": {
#                     "replica1": {
#                         "ansible_connection": "ssh",
#                         "ansible_host": "192.168.181.129",
#                         "ansible_port": 22,
#                         "ansible_ssh_private_key_file": ".vagrant/machines/vm2/vmware_fusion/private_key",
#                         "ansible_user": "vagrant",
#                     }
#                 }
#             },
#         }
#         mock_safe_load.return_value = mock_data
#         mock_impacted_host_groups.return_value = [
#             "pythonwebservers",
#             "postgresmainserver",
#         ]

#         response = pp.check_hosts(default_ip="10.10.10.10")
#         assert response is True


class TestPythonPostgresFunctions(unittest.TestCase):
    def test_get_input_user_with_user_input(self):
        with patch("builtins.input", return_value="10.10.09.01/67"):
          assert get_user_input("ip", "10.10.10.10/56") == "10.10.09.01/67"

    def test_get_input_user_with_default_input(self):
        with patch("builtins.input", return_value=""):
          assert get_user_input("ip", "10.10.10.10/56") == "10.10.10.10/56"     

    def test_get_user_confirmation_with_yes(self):
        with patch("builtins.input", return_value="y"):
          assert get_user_confirmation("ip") == False

    def test_get_user_confirmation_with_no(self):
        with patch("builtins.input", return_value="n"):
          assert get_user_confirmation("ip") == True

    def test_get_user_confirmation_with_invalid_input_then_no(self):
        with patch("builtins.input", side_effect=['t', 'n']):
          assert get_user_confirmation("ip") == True         

    def test_get_user_confirmation_with_invalid_input_then_yes(self):
        with patch("builtins.input", side_effect=['t', 'y']):
          assert get_user_confirmation("ip") == False    

    @patch("yaml.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_open, mock_yaml_dump):
        directory = "test/commands"
        filename = "test.yaml"
        data = {"ip": "10.10.10.1/98"}
        write_to_file(directory, filename, data)

        mock_open.assert_called_once_with(os.path.join(directory, filename), "w")
        mock_yaml_dump.assert_called_once_with(data, mock_open.return_value.__enter__.return_value)

         
    def test_write_to_file_with_temp_file(self):
        directory = tempfile.mkdtemp()
        filename = "test.yaml"
        data = {"ip": "10.10.10.1/98"}
        write_to_file(directory, filename, data)

        # Now read the file and check its contents
        with open(os.path.join(directory, filename), 'r') as file:
            read_data = yaml.safe_load(file)

        self.assertEqual(data, read_data)

    

          
