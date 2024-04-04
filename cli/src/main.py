import typer
from InquirerPy import inquirer
from constants import KNEE_DEFAULTS, CUSTOM_SELECTIONS
from commands.custom_selections import CustomSelections
from constants import SUBCOMMAND_TO_DESCRIPTION_MAP, COMMAND_TO_CATEGORY_MAP
from input_selection import custom_selections, get_environment, initial_input_selection
from commands.help_command import version_callback, help_callback, command_callback

app = typer.Typer()

@app.callback(invoke_without_command=True)
def help_command(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback),
    command: bool = typer.Option(None, "--command", "-c", callback=command_callback),
    help: bool = typer.Option(None, "--help", "-h", callback=help_callback),
):
    if ctx.invoked_subcommand is None and not (version or command or help):
        typer.echo(typer.style("Invalid option. Use '--help' for available options.", fg=typer.colors.MAGENTA, bold=True))
    return

@app.command()
def execute():
    option = initial_input_selection()
    server = db = additional_service = None
    if option == KNEE_DEFAULTS:
        command = inquirer.select(
            message="Please select a command:",
            choices=list(COMMAND_TO_CATEGORY_MAP.keys()),
            default="python-postgres",
        ).execute()
        if COMMAND_TO_CATEGORY_MAP.get(command):
            server = COMMAND_TO_CATEGORY_MAP[command]["server"]
            db = COMMAND_TO_CATEGORY_MAP[command]["db"]
        else:
            typer.secho("We are working hard for this command to be available soon!....", bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)
    elif option == CUSTOM_SELECTIONS:
        db, server, additional_service = custom_selections()
        if db is None and server is None and additional_service is None:
            typer.secho("Please select a valid option", bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)
            raise typer.Abort()
    else:
        typer.secho("We are working hard for this command to be available soon!....", bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)
    environment = get_environment()
    custom_inputs = CustomSelections(environment=environment, db_client_class=db, server_class=server, additional_service=additional_service)
    custom_inputs.check_defaults()
    typer.echo("Done!")

if __name__ == "__main__":
    app()
