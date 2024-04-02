import typer
from InquirerPy import inquirer
from commands.python_postgres import PythonPostgres
from commands.node_mongo import NodeMongo
from commands.golang_mongo import GolangMongo
from commands.custom_selections import CustomSelections
from command_class_mapping import COMMAND_TO_CATEGORY_MAP
from input_selection import custom_selections, get_environment, initial_input_selection

app = typer.Typer()

@app.command()
def list_command():
    commands = ["python-postgres", "give-ssh-access", "rails-with-postgres"]
    for command in commands:
        typer.echo(command)

@app.command()
def describe(command: str):
    descriptions = {
        "pp": "Python Server, Postgres DB. This commands sets up python server with a PostgreSQL src.database.",
        "give-ssh-access": "This command grants SSH access to a user.",
        "postgres": "This command sets up a PostgreSQL src.database.",
        "postgres-with-replica": "This command sets up a PostgreSQL database with a replica.",
    }
    typer.echo(descriptions.get(command, "Command not found"))

@app.command()
def execute():
    option = initial_input_selection()
    server = db = additional_service = None
    if option == "knee-defaults":
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
    elif option == "custom-selections":
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
