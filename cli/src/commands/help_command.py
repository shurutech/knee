import typer
from constants import SUBCOMMAND_DESCRIPTION_MAP, COMMANDS_DESCRIPTION_MAP

def version_callback(value: bool):
    if value:
        typer.echo("Knee 1.0.0")
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
        typer.echo("-v, --version : Show the version and exit.")
        typer.echo("-c, --command : Show the commands and exit.")
        typer.echo("-h, --help : Show this message and exit.")
        typer.echo()
        typer.echo(typer.style("Commands:", fg=typer.colors.BRIGHT_MAGENTA))
        for command, description in COMMANDS_DESCRIPTION_MAP.items():
            typer.echo(f"{command} : {description}")
        raise typer.Exit()
