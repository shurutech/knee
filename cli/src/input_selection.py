from InquirerPy import inquirer
from constants import INITIAL_OPTION_KNEE_DEFAULTS, INITIAL_OPTION_CUSTOM_SELECTIONS


def custom_selections():
    db = inquirer.select(
        message="Select database:",
        choices=["postgresql", "mongodb", "mysql",None],
        default="postgres",
    ).execute()
    server = inquirer.select(
        message="Select backend:",
        choices=["python", "nodejs", "golang","ruby",None],
        default="python",
    ).execute()
    additional_services = inquirer.select(
        message="Select additional services:",
        choices=["redis",None],
        default="redis",
    ).execute()
    return db, server, additional_services

def get_environment():
    return inquirer.select(
        message="Select environment to execute command:",
        choices=["local","staging", "production"],
        default="staging",
    ).execute()

def initial_input_selection():
    return inquirer.select(
        message="Please select an option:",
        choices=[INITIAL_OPTION_KNEE_DEFAULTS, INITIAL_OPTION_CUSTOM_SELECTIONS],
    ).execute()