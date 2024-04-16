import unittest
from unittest.mock import patch, MagicMock
from src.utils.runner import run_playbook


class TestRunner(unittest.TestCase):
    @patch("ansible_runner.run")
    def test_run_playbook_success(self, mock_run):
        mock_run.return_value = MagicMock(status="success")
        run_playbook("test_playbook", "test_environment")
        mock_run.assert_called_once_with(private_data_dir="./", playbook="playbooks/test_playbook", inventory="inventories/test_environment")

    @patch("ansible_runner.run")
    def test_run_playbook_failure(self, mock_run):
        mock_run.return_value = MagicMock(status="failed")
        with self.assertRaises(Exception):
            run_playbook("test_playbook", "test_environment")
        mock_run.assert_called_once_with(private_data_dir="./", playbook="playbooks/test_playbook", inventory="inventories/test_environment")
