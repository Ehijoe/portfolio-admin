"""Database interface module."""
import pymongo

from flask import current_app, g


class DataBase:
    """Database interface."""

    def __init__(self, *args, **kwargs):
        """Initialize the database."""
        self.client = pymongo.MongoClient(*args, **kwargs)
        self.db = self.client[current_app.config['DATABASE']]
        self.projects = self.db['projects']


def get_db() -> DataBase:
    """Create database if it doesn't exist and return it."""
    if 'db' not in g:
        g.db = DataBase()

    return g.db
