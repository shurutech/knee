import typer
from src.utils.constants.constants import SUBCOMMAND_DESCRIPTION_MAP, COMMANDS_DESCRIPTION_MAP, KNEE_VERSION
from src.utils.constants.prompt import Prompt


def version_callback(value: bool):
    if value:
        typer.echo(KNEE_VERSION)
        raise typer.Exit()

def command_callback(value: bool):
    if value:
        for category, data in SUBCOMMAND_DESCRIPTION_MAP.items():
            typer.echo(f"\n{category} :{data['description']}\n")
            max_length = max(len(command) for command in data['commands'].keys())
            for command, description in data['commands'].items():
                typer.echo(f"{command:<{max_length}} : {description}")
        raise typer.Exit()

def help_callback(value: bool):
    if value:
        typer.echo(typer.style("Options:", fg=typer.colors.BRIGHT_MAGENTA))
        typer.echo(Prompt.SHOW_VERSION_MESSAGE)
        typer.echo(Prompt.SHOW_COMMAND_MESSAGE)
        typer.echo(Prompt.SHOW_HELP_MESSAGE)
        typer.echo()
        typer.echo(typer.style("Commands:", fg=typer.colors.BRIGHT_MAGENTA))
        for command, description in COMMANDS_DESCRIPTION_MAP.items():
            typer.echo(f"{command} : {description}")
        raise typer.Exit()
