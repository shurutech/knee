import os
import unittest
from unittest.mock import patch, mock_open
from src.utils.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    @patch("yaml.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_file_open, mock_yaml_dump):
        directory = "test_directory"
        filename = "test_file.yml"
        data = {"test": "data"}
        file_manager = FileManager()
        file_manager.write_to_file(directory, filename, data)

        mock_file_open.assert_called_once_with(os.path.join(directory, filename), "w")
        mock_yaml_dump.assert_called_once_with(data, mock_file_open())

    @patch("yaml.safe_load", return_value={"test": "data"})
    @patch("builtins.open", new_callable=mock_open, read_data="test: data")
    def test_read_from_file(self, mock_file_open, mock_yaml_safe_load):
        directory = "test_directory"
        filename = "test_file.yml"
        expected_data = {"test": "data"}
        file_manager = FileManager()
        actual_data = file_manager.read_from_file(directory, filename)

        mock_file_open.assert_called_once_with(os.path.join(directory, filename), "r")
        self.assertEqual(actual_data, expected_data)
