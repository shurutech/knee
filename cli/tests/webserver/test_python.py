from src.webserver.python import Python
import unittest
from unittest.mock import patch, call


class TestPython(unittest.TestCase):
    @patch("src.webserver.python.FileManager.read_from_file")
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

    @patch("src.webserver.python.load_configuration")
    def test_update_configuration(self, mock_load_configuration):
        python = Python()
        mock_load_configuration.return_value = {
            "pythonwebservers.yml": {"python_port": "5434"}
        }
        python.update_configuration()
        self.assertEqual(python.configs["pythonwebservers.yml"]["python_port"], "5434")

    @patch("src.webserver.python.FileManager.write_to_file")
    @patch("src.webserver.python.FileManager.read_from_file")
    @patch("src.webserver.python.run_playbook")
    def test_apply_configuration_called_with_expected_arguments(
        self,
        mock_run_playbook,
        mock_read_from_file,
        mock_write_to_file,
    ):
        mock_read_from_file.return_value = {"python_version": "3.8.1"}
        python = Python()
        python.apply_configuration()
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

    @patch("src.webserver.python.run_playbook")
    @patch("src.webserver.python.FileManager.write_to_file")
    @patch("src.webserver.python.FileManager.read_from_file")
    def test_apply_configuration_when_it_is_called(
        self, mock_read_from_file, mock_write_to_file, mock_run_playbook
    ):
        mock_read_from_file.return_value = {"python_version": "3.8.1"}
        python = Python()
        python.apply_configuration()
        mock_run_playbook.assert_called()

    @patch("src.webserver.python.run_playbook")
    @patch("src.webserver.python.FileManager.write_to_file")
    @patch("src.webserver.python.FileManager.read_from_file")
    def test_apply_configuration_when_it_is_not_called(
        self, mock_read_from_file, mock_write_to_file, mock_run_playbook
    ):
        mock_read_from_file.return_value = {"python_version": "3.8.1"}
        mock_run_playbook.side_effect = Exception("An error occurred")
        python = Python()
        with self.assertRaises(Exception) as context:
            python.apply_configuration()

        self.assertTrue("An error occurred" in str(context.exception))

   

