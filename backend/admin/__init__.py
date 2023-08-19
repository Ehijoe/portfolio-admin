"""Admin view for managing projects."""
from flask import (Blueprint, render_template, session, url_for, redirect,
                   request)
from functools import wraps
from werkzeug.security import check_password_hash

from ..db import get_db

admin_bp = Blueprint('admin', __name__, static_url_path='/admin-static',
                     template_folder='templates', static_folder='static')


def protected(route):
    """Require authentication for a route."""
    @wraps(route)
    def f(*args, **kwargs):
        if not session.get("logged_in", False):
            return redirect(url_for('admin.login'))
        return route(*args, **kwargs)
    return f


@admin_bp.route('/login', methods=["GET", "POST"])
def login():
    """Login route."""
    if request.method == "POST":
        db = get_db()
        password = request.form.get('password')
        password_hash = db.db['passwords'].find_one({}).get('hash')
        if password is None or password == "":
            print("Empty password")
            return redirect(url_for('admin.login'))
        if password_hash is None:
            print("No password set")
            return redirect(url_for('admin.login'))
        if check_password_hash(password_hash, password):
            print("Logged in successfully")
            session['logged_in'] = True
            return redirect(url_for('admin.index'))
        print("Wrong password")
        return redirect(url_for('admin.login'))
    return render_template('login.html')


@admin_bp.route('/logout')
def logout():
    """Log out the user."""
    session.clear()
    return redirect(url_for('admin.login'))


@admin_bp.route('/projects/add', methods=["POST"])
def add_project():
    """Add a new project."""
    tags = request.form.getlist("tags[]")
    print(tags)
    return redirect(url_for('admin.index'))


@admin_bp.route('/')
@protected
def index():
    """Render the home page for the admin dashboard."""
    db = get_db()
    projects = db.projects.find()
    return render_template('index.html', projects=projects)
