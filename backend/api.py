"""API views."""
from flask import Blueprint, request, jsonify
from flask_cors import CORS

from .db import get_db

api_bp = Blueprint('api', __name__, url_prefix='/api')

CORS(api_bp)


@api_bp.route('/projects')
def get_projects():
    """Get list of projects."""
    number = request.args.get('number')
    tags = request.args.getlist('tags')
    try:
        number = int(number)
    except (TypeError, ValueError):
        number = 3
    db = get_db()
    if len(tags) == 0:
        projects = db.projects.find({})
    else:
        projects = db.projects.find({"tags": {"$all": tags}})
    projects = list(projects)[:number]
    for project in projects:
        del project["_id"]
    return jsonify(projects)
