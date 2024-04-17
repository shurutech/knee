import tempfile
from src.utils.utils import (
    get_user_input,
    get_user_confirmation,
    get_hosts_configuration_parameters,
)
from unittest.mock import patch, mock_open, MagicMock
import unittest
import yaml
import os


class TestUtils(unittest.TestCase):
    def test_get_input_user_with_user_input(self):
        with patch("builtins.input", return_value="10.10.09.01/67"):
            assert get_user_input("ip", "10.10.10.10/56") == "10.10.09.01/67"

    def test_get_input_user_with_default_input(self):
        with patch("builtins.input", return_value=""):
            assert get_user_input("ip", "10.10.10.10/56") == "10.10.10.10/56"

    @patch("InquirerPy.inquirer.confirm")
    def test_get_user_confirmation_input_true(self, mock_confirm):
        mock_confirmation = MagicMock()
        mock_confirm.return_value = mock_confirmation
        mock_confirmation.execute.return_value = True
        key = "test_key"
        result = get_user_confirmation(key)
        mock_confirm.assert_called_once_with(
            message=f"Do you want to keep the default value for {key}?", default=True
        )
        mock_confirmation.execute.assert_called_once()
        self.assertEqual(result, False)

    @patch("InquirerPy.inquirer.confirm")
    def test_get_user_confirmation_input_False(self, mock_confirm):
        mock_confirmation = MagicMock()
        mock_confirm.return_value = mock_confirmation
        mock_confirmation.execute.return_value = False
        key = "test_key"
        result = get_user_confirmation(key)
        mock_confirm.assert_called_once_with(
            message=f"Do you want to keep the default value for {key}?", default=True
        )
        mock_confirmation.execute.assert_called_once()
        self.assertEqual(result, True)

    def test_host_configuration_parameters_default_input(self):
        selected_host_groups = ["webservers", "databasemainserver"]
        hosts_config = {"webservers": {"hosts": {"web1": {"ip": "10.10.10.10/56"}}}}
        with patch("builtins.input", return_value=""):
            result = get_hosts_configuration_parameters(selected_host_groups, hosts_config)
            self.assertEqual(result, hosts_config)

    def test_host_configuration_parameters_user_input(self):
        selected_host_groups = ["webservers", "databasemainserver"]
        hosts_config = {"webservers": {"hosts": {"web1": {"ip": "10.10.10.10/56"}}}}
        with patch("builtins.input", return_value="10.10.1.1/47"):
            result = get_hosts_configuration_parameters(selected_host_groups, hosts_config)
            self.assertEqual(
                result["webservers"]["hosts"]["web1"]["ip"], "10.10.1.1/47"
            )
