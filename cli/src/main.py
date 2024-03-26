import typer
from InquirerPy import inquirer
from commands.python_postgres import PythonPostgres
from commands.node_mongo import NodeMongo
from commands.golang_mongo import GolangMongo
from commands.custom_selections import CustomSelections
from command_class_mapping import COMMAND_TO_CLASS_MAP

app = typer.Typer()

def custom_selections():
    db = inquirer.select(
        message="Select database:",
        choices=["postgresql", "mongodb", "mysql",None],
        default="postgres",
    ).execute()
    backend = inquirer.select(
        message="Select backend:",
        choices=["python", "nodejs", "golang","ruby",None],
        default="python",
    ).execute()
    return db, backend

@app.command()
def list():
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
    option = inquirer.select(
        message="Please select an option:",
        choices=["knee-defaults", "custom-selections"],
    ).execute()
    if option == "knee-defaults":
        command = inquirer.select(
            message="Please select a command:",
            choices=[key for key in COMMAND_TO_CLASS_MAP.keys()],
            default="python-postgres",
        ).execute()

        environment= inquirer.select(
        message="Select environment to execute command:",
        choices=["local","staging", "production"],
        default="Staging",
        ).execute()

        if COMMAND_TO_CLASS_MAP.get(command):
            command_class = COMMAND_TO_CLASS_MAP[command]
            command_class(environment = environment).check_defaults()
        else:
            typer.secho("We are working hard for this command to be available soon!....", bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)
    elif option == "custom-selections":
        db, server = custom_selections()
        if db is None and server is None:
            typer.secho("Please select a valid option", bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)
            raise typer.Abort()
        environment= inquirer.select(
        message="Select environment to execute command:",
        choices=["local","staging", "production"],
        default="staging",
        ).execute()
        custom_inputs = CustomSelections(environment=environment, db_client_class=db, server_class=server)
        custom_inputs.check_defaults()
        typer.echo(f"Setting up {db} database with {server} server and client...")
    else:
        typer.secho("We are working hard for this command to be available soon!....", bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)

if __name__ == "__main__":
    app()
