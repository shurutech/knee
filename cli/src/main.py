import typer
from InquirerPy import inquirer
from framework.system_framework import SystemFramework
from utils.constants.constants import COMMAND_SERVICE_MAP
from input_selection import custom_selections, get_environment, get_user_input
from callback import version_callback, help_callback, command_callback
from utils.constants.prompt import Prompt
from utils.constants.enum import InitialOption


app = typer.Typer()

@app.callback(invoke_without_command=True)
def help_command(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback),
    command: bool = typer.Option(None, "--command", "-c", callback=command_callback),
    help: bool = typer.Option(None, "--help", "-h", callback=help_callback),
):
    if ctx.invoked_subcommand is None and not (version or command or help):
        typer.echo(typer.style(Prompt.INVALID_OPTION.value, fg=typer.colors.MAGENTA, bold=True))
    return

@app.command()
def execute():
    user_selections = {}
    user_input = get_user_input()
    match user_input:
        case InitialOption.KNEE_DEFAULTS.value:
            command = inquirer.select(
                message=Prompt.SELECT_COMMAND.value,
                choices=list(COMMAND_SERVICE_MAP.keys()),
                default="python-postgres",
            ).execute()
            if COMMAND_SERVICE_MAP.get(command):
                user_selections = {
                    "database": COMMAND_SERVICE_MAP[command]["db"],
                    "webserver": COMMAND_SERVICE_MAP[command]["server"]
                }
        case InitialOption.CUSTOM_SELECTIONS.value:
            user_selections = custom_selections()
            if all(value is None for value in user_selections.values()):
                typer.secho(Prompt.SELECT_VALID_OPTION.value, bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)
                raise typer.Abort()
        case _:
            typer.secho(Prompt.COMMAND_NOT_AVAILABLE.value, bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)

    environment = get_environment()
    system_framework = SystemFramework(environment=environment, user_selections=user_selections)
    if system_framework.init():
        typer.echo("Done!")

if __name__ == "__main__":
    app()
