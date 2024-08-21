import click
import pytest
from commandlib import Command
from flask.cli import FlaskGroup

from antipodal import create_app
from dotenv import load_dotenv

cli = FlaskGroup(create_app=create_app)

psql = Command("psql")

load_dotenv()


@cli.command()
def test() -> None:
    """use to test things"""
    pytest.main(args=["tests/", "--pdb"])


@cli.command()
@click.argument("what")
def setup(what) -> None:
    """
    use to set things up
    :param what: db
    """
    if what == "db":
        psql("--command=CREATE DATABASE antipodal").run()
        psql("--command=CREATE USER antipodal WITH PASSWORD 'password'").run()
        psql("--command=ALTER ROLE antipodal SUPERUSER").run()
        psql("--command=GRANT ALL PRIVILEGES ON DATABASE antipodal TO antipodal").run()
    else:
        click.echo("No such thing to setup")


@cli.command()
@click.argument("what")
def drop(what) -> None:
    """
    use to drop things
    :param what: db
    """
    if what == "db":
        psql("--command=DROP DATABASE antipodal").run()
        psql("--command=DROP USER antipodal").run()
    else:
        click.echo("No such thing to drop")


if __name__ == "__main__":
    cli()
