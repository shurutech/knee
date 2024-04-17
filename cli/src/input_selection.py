from InquirerPy import inquirer
from utils.constants.prompt import Prompt
from utils.constants.enum import Database, Webserver, CachingTool, Environment, InitialOption


def custom_selections():
    db = inquirer.select(
        message=Prompt.SELECT_DATABASE.value,
        choices=[Database.POSTGRESQL.value, Database.MONGODB.value, Database.MYSQL.value, None],
        default=Database.POSTGRESQL.value,
    ).execute()
    webserver = inquirer.select(
        message=Prompt.SELECT_WEBSERVER.value,
        choices=[Webserver.PYTHON.value, Webserver.NODEJS.value, Webserver.RUBY.value, Webserver.GOLANG.value, None],
        default=Webserver.PYTHON.value,
    ).execute()
    caching_tool = inquirer.select(
        message=Prompt.SELECT_CACHING_TOOL.value,
        choices=[CachingTool.REDIS.value, None],
        default=CachingTool.REDIS.value,
    ).execute()
    user_selections = {
        "database": db,
        "webserver": webserver,
        "caching_tool": caching_tool
    }
    return user_selections

def get_environment():
    return inquirer.select(
        message=Prompt.SELECT_ENVIRONMENT.value,
        choices=[Environment.LOCAL.value, Environment.STAGING.value, Environment.PRODUCTION.value],
        default=Environment.LOCAL.value,
    ).execute()

def get_user_input():
    return inquirer.select(
        message=Prompt.SELECT_OPTION.value,
        choices=[InitialOption.KNEE_DEFAULTS.value, InitialOption.CUSTOM_SELECTIONS.value],
    ).execute()

