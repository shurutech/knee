import pytest
from cli.src.commands.python_postgres import PythonPostgres
from unittest.mock import patch


class TestPythonPostgres:
    def test_check_hosts_raise_argument_error_if_default_ip(self):
        pp = PythonPostgres(environment="local")
        with pytest.raises(ValueError) as message:
            pp.check_hosts()
        assert (
            "Host: webserver1, Ansible Host: 192.168.181.128 is set to default IP. Please set the ansible_host for the host."
            in str(message.value)
        )

    def test_check_hosts_does_not_raise_argument_error_if_not_default_ip(self):
        pp = PythonPostgres(environment="local")
        response = pp.check_hosts(default_ip="10.10.10.10")
        assert response is True

    @patch("cli.src.commands.python_postgres.IMPACTED_HOST_GROUPS")
    @patch("cli.src.commands.python_postgres.yaml.safe_load")
    def test_check_hosts_default_ip_present_in_non_impacted_host_group(
        self, mock_safe_load, mock_impacted_host_groups
    ):
        pp = PythonPostgres(environment="local")
        mock_data = {
            "postgresmainserver": {
                "hosts": {
                    "mainserver": {
                        "ansible_connection": "ssh",
                        "ansible_host": "192.168.181.128",
                        "ansible_port": 22,
                        "ansible_ssh_private_key_file": ".vagrant/machines/vm1/vmware_fusion/private_key",
                        "ansible_user": "vagrant",
                    }
                }
            },
            "postgresreplicaservers": {
                "hosts": {
                    "replica1": {
                        "ansible_connection": "ssh",
                        "ansible_host": "192.168.181.129",
                        "ansible_port": 22,
                        "ansible_ssh_private_key_file": ".vagrant/machines/vm2/vmware_fusion/private_key",
                        "ansible_user": "vagrant",
                    }
                }
            },
        }
        mock_safe_load.return_value = mock_data
        mock_impacted_host_groups.return_value = [
            "pythonwebservers",
            "postgresmainserver",
        ]

        response = pp.check_hosts(default_ip="192.168.181.128")
        assert response is True

    @patch("cli.src.commands.python_postgres.IMPACTED_HOST_GROUPS")
    @patch("cli.src.commands.python_postgres.yaml.safe_load")
    def test_check_hosts_not_default_ip_and_non_impacted_host_group(
        self, mock_safe_load, mock_impacted_host_groups
    ):
        pp = PythonPostgres(environment="local")
        mock_data = {
            "postgresmainserver": {
                "hosts": {
                    "mainserver": {
                        "ansible_connection": "ssh",
                        "ansible_host": "192.168.181.128",
                        "ansible_port": 22,
                        "ansible_ssh_private_key_file": ".vagrant/machines/vm1/vmware_fusion/private_key",
                        "ansible_user": "vagrant",
                    }
                }
            },
            "postgresreplicaservers": {
                "hosts": {
                    "replica1": {
                        "ansible_connection": "ssh",
                        "ansible_host": "192.168.181.129",
                        "ansible_port": 22,
                        "ansible_ssh_private_key_file": ".vagrant/machines/vm2/vmware_fusion/private_key",
                        "ansible_user": "vagrant",
                    }
                }
            },
        }
        mock_safe_load.return_value = mock_data
        mock_impacted_host_groups.return_value = [
            "pythonwebservers",
            "postgresmainserver",
        ]

        response = pp.check_hosts(default_ip="10.10.10.10")
        assert response is True
