from src.additional_services.redis import Redis
import unittest
from unittest.mock import patch, call


class TestRedis(unittest.TestCase):
    @patch("src.additional_services.redis.FileManager.read_from_file")
    def test_initialiser_with_file(self, mock_read_from_file):
        mock_read_from_file.return_value = {
            "rediswebservers.yml": {"redis_port": "6379"}
        }
        redis = Redis()
        self.assertEqual(
            redis.configs["redisserver.yml"]["rediswebservers.yml"]["redis_port"],
            "6379",
        )

    @patch("src.additional_services.redis.load_configuration")
    def test_parameter_configuration(self, mock_load_configuration):
        redis = Redis()
        redis.configs = {
            "rediswebservers.yml": {"redis_port": "6379"}
        }
        mock_load_configuration.return_value = {
            "rediswebservers.yml": {"redis_port": "6380"}
        }
        redis.parameter_configuration()
        mock_load_configuration.assert_called_once_with( {
            "rediswebservers.yml": {"redis_port": "6379"}
        })
        self.assertEqual(
              redis.configs["rediswebservers.yml"]["redis_port"],
              "6380",
          )

    @patch("src.additional_services.redis.load_configuration")
    def test_parameter_configuration_raises_error(self, mock_load_configuration):
        redis = Redis()
        redis.configs = {
            "redis.yml": {"redis_port": "6379"}
        }
        mock_load_configuration.side_effect = Exception("Error")
        with self.assertRaises(Exception) as context:
            redis.parameter_configuration()
        self.assertTrue('Error' in str(context.exception))

    @patch("src.additional_services.redis.FileManager.write_to_file")
    @patch("src.additional_services.redis.run_playbook")
    def test_write_configuration_and_run_playbook(self, mock_run_playbook, mock_write_to_file):
        redis = Redis()
        redis.CONFIG_FILES = ["redisserver.yml"]
        redis.configs = {
             "redisserver.yml": {"redis_port": "6379"}
        }
        redis.write_configuration_and_run_playbook()
        mock_write_to_file.assert_called_once_with(
            "playbooks/group_vars", "redisserver.yml", {"redis_port": "6379"}
        )
        mock_run_playbook.assert_any_call("redis_server.yml", "local")

    @patch("src.additional_services.redis.run_playbook")
    @patch("src.additional_services.redis.FileManager.write_to_file")
    @patch("src.additional_services.redis.FileManager.read_from_file")
    def test_write_configuration_and_run_playbook_when_it_is_called(
        self, mock_read_from_file, mock_write_to_file, mock_run_playbook
    ):
        mock_read_from_file.return_value = {"redis_port": "6379"}
        redis = Redis()
        redis.write_configuration_and_run_playbook()
        mock_run_playbook.assert_called()

    @patch("src.additional_services.redis.run_playbook")
    @patch("src.additional_services.redis.FileManager.write_to_file")
    @patch("src.additional_services.redis.FileManager.read_from_file")
    def test_write_configuration_and_run_playbook_raises_error(
        self, mock_read_from_file, mock_write_to_file, mock_run_playbook
    ):
        mock_read_from_file.return_value = {"redis_port": "6379"}
        mock_run_playbook.side_effect = Exception("An error occurred")
        redis = Redis()
        with self.assertRaises(Exception) as context:
            redis.write_configuration_and_run_playbook()

        self.assertTrue("An error occurred" in str(context.exception))



        

    