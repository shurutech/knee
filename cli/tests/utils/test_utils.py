import tempfile
from src.utils.utils import get_user_input, get_user_confirmation, write_to_file, read_from_file
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
        mock_confirm.assert_called_once_with(message=f"Do you want to keep the default value for {key}?", default=True)
        mock_confirmation.execute.assert_called_once()
        self.assertEqual(result, False)

    @patch("InquirerPy.inquirer.confirm")
    def test_get_user_confirmation_input_False(self, mock_confirm):
        mock_confirmation = MagicMock()
        mock_confirm.return_value = mock_confirmation
        mock_confirmation.execute.return_value = False
        key = "test_key"
        result = get_user_confirmation(key)
        mock_confirm.assert_called_once_with(message=f"Do you want to keep the default value for {key}?", default=True)
        mock_confirmation.execute.assert_called_once()
        self.assertEqual(result, True)        

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
        with open(os.path.join(directory, filename), 'r') as file:
            read_data = yaml.safe_load(file)

        self.assertEqual(data, read_data)
    
    
    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open, read_data="test data")
    def test_read_from_file(self, mock_open, mock_safe_load):
        directory = "test/commands"
        filename = "test.yaml"
        read_from_file(directory, filename)
        mock_open.assert_called_once_with(os.path.join(directory, filename), "r")
        mock_safe_load.assert_called_once_with(mock_open.return_value.__enter__.return_value)
       