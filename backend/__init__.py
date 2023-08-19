"""Backend."""
import os

from flask import Flask


def create_app(test_config=None):
    """App factory."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='portfolio_db',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .commands import add_commands
    add_commands(app)

    from .api import api_bp
    app.register_blueprint(api_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
