import click
from commandlib import Command
from flask.cli import FlaskGroup
import pytest
from antipodal import create_app

cli = FlaskGroup(create_app=create_app)

psql = Command("psql")
git = Command("git")


@cli.command(name="gac")
@click.argument("message")
def git_add_and_commit(message):
    exit_code = pytest.main(args=["tests/"])
    if exit_code != 0:
        click.echo("# ************************************************* #")
        prompt = click.prompt("tests failed: do you want to continue? (y)es OR any other key for no")
        if prompt.lower() not in ("yes", "y"):
            return
        else:
            click.echo("commit with test failures")
    else:
        git.with_trailing_args("commit", "-am", message).run()


@cli.command()
def test():
    """use to test things"""
    pytest.main(args=["tests/", "--pdb"])


@cli.command()
@click.argument("what")
def setup(what):
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
def drop(what):
    """
    use to drop things
    :param what: db
    """
    if what == "db":
        psql(f"--command=DROP DATABASE antipodal").run()
        psql(f"--command=DROP USER antipodal").run()
    else:
        click.echo("No such thing to drop")


if __name__ == "__main__":
    cli()
