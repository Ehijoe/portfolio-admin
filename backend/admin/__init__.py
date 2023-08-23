"""Admin view for managing projects."""
from flask import (Blueprint, render_template, session, url_for, redirect,
                   request, current_app, send_from_directory)
from functools import wraps
from werkzeug.security import check_password_hash
import uuid
import os
from bson.objectid import ObjectId

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


def save_file(image_file):
    """Save a project image."""
    extension = image_file.filename.split('.')[-1]
    if extension not in {"png", "jpg", "jpeg", "gif"}:
        return None
    name = f"{uuid.uuid4()}.{extension}"
    os.makedirs(os.path.join(current_app.instance_path, "images"),
                exist_ok=True)
    image_file.save(os.path.join(current_app.instance_path, "images", name))
    return name


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


@admin_bp.route('/projects/delete/<string:id>')
def delete_project(id):
    """Delete the project with a given id."""
    print(id)
    db = get_db()
    result = db.projects.delete_one({"_id": ObjectId(id)})
    print(result.raw_result)
    return redirect(url_for('admin.index'))


@admin_bp.route('/projects/add', methods=["POST"])
def add_project():
    """Add a new project."""
    tags = request.form.getlist("tags[]")
    db = get_db()
    project = {"tags": tags}
    for field in ["title", "description"]:
        value = request.form.get(field)
        if value in [None, ""]:
            print(f"{field} is missing")
            return redirect(url_for('admin.index'))
        else:
            project[field] = value
    for field in ["source", "demo"]:
        value = request.form.get(field)
        if value not in [None, ""]:
            project[field] = value
    if "image" not in request.files:
        return redirect((url_for('admin.index')))
    project["image"] = save_file(request.files["image"])
    if project["image"] is None:
        return redirect(url_for('admin.index'))
    db.projects.insert_one(project)
    return redirect(url_for('admin.index'))


@admin_bp.route('/images/<string:filename>')
@protected
def images(filename):
    """Serve the project images."""
    return send_from_directory(
        os.path.join(current_app.instance_path, 'images'),
        filename,
    )


@admin_bp.route('/')
@protected
def index():
    """Render the home page for the admin dashboard."""
    db = get_db()
    projects = list(db.projects.find())
    for project in projects:
        project["id"] = str(project["_id"])
        del project["_id"]
    return render_template('index.html', projects=projects)
