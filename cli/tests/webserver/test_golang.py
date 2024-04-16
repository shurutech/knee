from src.webserver.golang import Golang
import unittest
from unittest.mock import patch, call
from src.utils.utils import load_configuration


class TestGolang(unittest.TestCase):
    def test_update_configuration_with_default_values(self):
        golang = Golang()
        golang.configs = {"golangwebservers.yml": {"golang_port": "8080"}}
        with patch("builtins.input", return_value=""):
            golang.configs = load_configuration(golang.configs)
        self.assertEqual(golang.configs["golangwebservers.yml"]["golang_port"], "8080")

    def test_update_configuration_with_user_input(self):
        golang = Golang()
        golang.configs = {"golangwebservers.yml": {"golang_port": "8080"}}
        with patch("builtins.input", return_value="8081"):
            golang.configs = load_configuration(golang.configs)
        self.assertEqual(golang.configs["golangwebservers.yml"]["golang_port"], "8081")

    @patch("src.webserver.golang.FileManager.write_to_file")
    @patch("src.webserver.golang.run_playbook")
    def test_apply_configuration_called_with_expected_arguments(
        self, mock_run_playbook, mock_write_to_file
    ):
        golang = Golang("local")
        golang.configs = {"golangwebservers.yml": {"golang_version": "1.21.3"}}
        golang.apply_configuration()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "golangwebservers.yml",
            {
                "golang_version": golang.configs["golangwebservers.yml"][
                    "golang_version"
                ]
            },
        )
        self.assertEqual(actual_call, expected_call)
        mock_run_playbook.assert_called_once_with("golang_server.yml", "local")
