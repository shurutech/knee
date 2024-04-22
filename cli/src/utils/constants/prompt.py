from enum import Enum


class Prompt(Enum):
    SELECT_VALID_OPTION = "Please select a valid option"
    SELECT_COMMAND = "Please select a command:"
    INVALID_OPTION = "Invalid option. Use '--help' for available options."
    COMMAND_NOT_AVAILABLE = "We are working hard for this command to be available soon!...."
    REPLICA_SETUP = "Do you want to setup a replica server? (Default= No) :: "
    CONFIGURATION_SETUP_CHANGE = "Do you want to change the configuration? (Default= Yes) :: "
    SELECT_DATABASE = "Select database:"
    SELECT_WEBSERVER = "Select tech stack for your backend application:"
    SELECT_CACHING_TOOL = "Select caching tool:"
    SELECT_ENVIRONMENT = "Select environment to execute command:"
    SELECT_OPTION = "Please select an option:"
    SHOW_VERSION_MESSAGE = "-v, --version : Show the version and exit."
    SHOW_COMMAND_MESSAGE = "-c, --command : Show the commands and exit."
    SHOW_HELP_MESSAGE = "-h, --help : Show this message and exit."
