from src.webserver.python import Python
import unittest
from unittest.mock import patch, call


class TestPython(unittest.TestCase):
    @patch("src.webserver.python.read_from_file")
    def test_initialiser_with_file(self, mock_read_from_file):
        mock_read_from_file.return_value = {
            "pythonwebservers.yml": {"python_port": "5555"}
        }
        python = Python()
        self.assertEqual(
            python.configs["pythonwebservers.yml"]["pythonwebservers.yml"][
                "python_port"
            ],
            "5555",
        )

    @patch("src.webserver.python.node_configuration_parameters")
    def test_parameter_configuration(self, mock_node_configuration_parameters):
        python = Python()
        mock_node_configuration_parameters.return_value = {
            "pythonwebservers.yml": {"python_port": "5434"}
        }
        python.parameter_configuration()
        self.assertEqual(python.configs["pythonwebservers.yml"]["python_port"], "5434")

    @patch("src.webserver.python.write_to_file")
    @patch("src.webserver.python.read_from_file")
    def test_write_configuration_parameters_called_with_expected_arguments(
        self,
        mock_read_from_file,
        mock_write_to_file,
    ):
        mock_read_from_file.return_value = {"python_version": "3.8.1"}
        python = Python()
        python.write_configuration_and_run_playbook()
        actual_call = mock_write_to_file.call_args
        expected_call = call(
            "playbooks/group_vars",
            "pythonwebservers.yml",
            {
                "python_version": python.configs["pythonwebservers.yml"][
                    "python_version"
                ]
            },
        )
        self.assertEqual(actual_call, expected_call)
