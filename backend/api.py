"""API views."""
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/projects')
def get_projects():
    """Get list of projects."""
    number = request.args.get('number')
    tags = request.args.getlist('tags')
    try:
        number = int(number)
    except (TypeError, ValueError):
        number = 3
    return jsonify(tags)
