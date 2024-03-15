import typer
from InquirerPy import inquirer
from commands.python_postgres import PythonPostgres
from commands.node_mongo import NodeMongo
from commands.golang_mongo import GolangMongo

app = typer.Typer()

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
    command = inquirer.select(
        message="Select command to execute:",
        choices=[
            "python-postgres",
            "react",
            "MERN",
            "golang-mongo",
            "golang-postgresql",
            "ruby-mysql",
            "python-mysql"
            "ruby-postgres"
            "python-mongo"
        ],
        default="python-postgres",
    ).execute()
    environment = inquirer.select(
        message="Select environment to execute command:",
        choices=["local","staging", "production"],
        default="staging",
    ).execute()
    typer.echo(f"Executing {command} on {environment} environment...")
    if command == "python-postgres":
     python_postgres = PythonPostgres(environment=environment)
     python_postgres.check_defaults()
    elif command == "MERN":
     node_mongo = NodeMongo(environment=environment) 
     node_mongo.check_defaults()
    elif command == "golang-mongo":
        golang_mongo = GolangMongo(environment=environment)
        golang_mongo.check_defaults() 
    else:
        typer.secho("We are working hard for this command to be available soon!....", bg=typer.colors.YELLOW, fg=typer.colors.WHITE, bold=True)

if __name__ == "__main__":
    app()
