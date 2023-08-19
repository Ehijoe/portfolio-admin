"""Command line commands."""
import click

from flask import Flask
from werkzeug.security import generate_password_hash

from .db import get_db


@click.command('set_password')
@click.option(
    "--password", prompt=True, hide_input=True,
    confirmation_prompt=True
)
def set_password(password):
    """Set the admin password for uploading projects."""
    db = get_db()
    passwords = db.db["passwords"]
    passwords.delete_many({})
    passwords.insert_one({"hash": generate_password_hash(password)})
    click.echo("Password changed")


def add_commands(app: Flask):
    """Add commands to flask app."""
    app.cli.add_command(set_password)
