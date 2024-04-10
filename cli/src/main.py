import typer
from InquirerPy import inquirer
from constants import INITIAL_OPTION_KNEE_DEFAULTS, INITIAL_OPTION_CUSTOM_SELECTIONS
from commands.custom_selections import CustomSystem
from constants import SUBCOMMAND_DESCRIPTION_MAP, COMMAND_SERVICE_MAP
from input_selection import custom_selections, get_environment, initial_input_selection
from commands.help_command import version_callback, help_callback, command_callback
import utils.constants.message_constants as MESSAGE

app = typer.Typer()

@app.callback(invoke_without_command=True)
def help_command(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback),
    command: bool = typer.Option(None, "--command", "-c", callback=command_callback),
    help: bool = typer.Option(None, "--help", "-h", callback=help_callback),
):
    if ctx.invoked_subcommand is None and not (version or command or help):
        typer.echo(typer.style(MESSAGE.INVALID_OPTION_PROMPT, fg=typer.colors.MAGENTA, bold=True))
    return

@app.command()
def execute():
    option = initial_input_selection()
    server = db = additional_service = None
    if option == INITIAL_OPTION_KNEE_DEFAULTS:
        command = inquirer.select(
            message=MESSAGE.SELECT_COMMAND_PROMPT,
            choices=list(COMMAND_SERVICE_MAP.keys()),
            default="python-postgres",
        ).execute()
        if COMMAND_SERVICE_MAP.get(command):
            server = COMMAND_SERVICE_MAP[command]["server"]
            db = COMMAND_SERVICE_MAP[command]["db"]
    elif option == INITIAL_OPTION_CUSTOM_SELECTIONS:
        db, server, additional_service = custom_selections()
        if db is None and server is None and additional_service is None:
            typer.secho(MESSAGE.SELECT_VALID_OPTION_PROMPT, bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)
            raise typer.Abort()
    else:
        typer.secho(MESSAGE.COMMAND_NOT_AVAILABLE, bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)
    environment = get_environment()
    custom_inputs = CustomSystem(environment=environment, db_client_class=db, server_class=server, additional_service=additional_service)
    custom_inputs.check_defaults()
    typer.echo("Done!")

if __name__ == "__main__":
    app()
