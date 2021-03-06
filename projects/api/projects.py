# -*- coding: utf-8 -*-
"""Projects blueprint."""

from flask import jsonify, request
from flask_smorest import Blueprint
from projects.controllers.projects import create_project, \
    get_project, update_project, delete_project, pagination_projects, \
    delete_multiple_projects
from projects.utils import to_snake_case

bp = Blueprint("projects", __name__)


@bp.route("", methods=["GET"])
@bp.paginate(page=0)
def handle_list_projects(pagination_parameters):
    name = request.args.get('name')
    order = request.args.get('order')
    pagination_parameters.item_count = 0
    projects = pagination_projects(name=name,
                                   page=pagination_parameters.page,
                                   page_size=pagination_parameters.page_size, order=order)
    return jsonify(projects)


@bp.route("", methods=["POST"])
def handle_post_projects():
    """Handles POST requests to /."""
    kwargs = request.get_json(force=True)
    kwargs = {to_snake_case(k): v for k, v in kwargs.items()}
    project = create_project(**kwargs)
    return jsonify(project)


@bp.route("<project_id>", methods=["GET"])
def handle_get_project(project_id):
    """Handles GET requests to /<project_id>."""
    return jsonify(get_project(uuid=project_id))


@bp.route("<project_id>", methods=["PATCH"])
def handle_patch_project(project_id):
    """Handles PATCH requests to /<project_id>."""
    kwargs = request.get_json(force=True)
    kwargs = {to_snake_case(k): v for k, v in kwargs.items()}
    project = update_project(uuid=project_id, **kwargs)
    return jsonify(project)


@bp.route("<project_id>", methods=["DELETE"])
def handle_delete_project(project_id):
    """Handles DELETE requests to /<project_id>."""
    project = delete_project(uuid=project_id)
    return jsonify(project)


@bp.route("/deleteprojects", methods=["POST"])
def handle_delete_projects():
    kwargs = request.get_json(force=True)
    return jsonify(delete_multiple_projects(kwargs))
