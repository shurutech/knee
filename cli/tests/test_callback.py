import unittest
from unittest.mock import patch, Mock
import typer
from src.callback import version_callback


class TestHelpCommand(unittest.TestCase):
    @patch('typer.echo')
    def test_version_callback(self, mock_echo):
        with self.assertRaises(typer.Exit):
            version_callback(True)
        mock_echo.assert_called_once_with("Knee 1.0.0")
