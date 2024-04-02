import typer
from constants import COMMAND_WITH_DESCRIPTION

def version_callback(value: bool):
    if value:
        typer.echo("Knee 1.0.0")
        raise typer.Exit()

def help_callback(value: bool):
    if value:
        for category, data in COMMAND_WITH_DESCRIPTION.items():
            typer.echo(f"\n{category} :{data['description']}\n")
            max_length = max(len(command) for command in data['commands'].keys())
            for command, description in data['commands'].items():
                typer.echo(f"{command:<{max_length}} : {description}")
        raise typer.Exit()

def help_command(app):
    @app.callback(invoke_without_command=True)
    def help(
        version: bool = typer.Option(None, "--version", callback=version_callback),
        help: bool = typer.Option(None, "--help", callback=help_callback),
    ):
        return