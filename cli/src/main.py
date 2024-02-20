import typer

from commands.python_postgres import PythonPostgres

app = typer.Typer()


@app.command()
def list():
    commands = ["python-postgres", "give-ssh-access", "rails-with-postgres"]
    for command in commands:
        typer.echo(command)


@app.command()
def describe(command: str):
    descriptions = {
        "pp": "Python Server, Postgres DB. This commands sets up python server with a PostgreSQL database.",
        "give-ssh-access": "This command grants SSH access to a user.",
        "postgres": "This command sets up a PostgreSQL database.",
        "postgres-with-replica": "This command sets up a PostgreSQL database with a replica.",
    }
    typer.echo(descriptions.get(command, "Command not found"))


@app.command()
def execute(command: str, staging: bool = False, production: bool = False):
    if not (staging or production):
        typer.echo("Please specify an environment by passing --staging or --production")
        raise typer.Exit(code=1)
    environment = "staging" if staging else "production"
    typer.echo(f"Executing {command} on {environment} environment...")
    pp = PythonPostgres(environment=environment)
    pp.check_defaults()


if __name__ == "__main__":
    app()
