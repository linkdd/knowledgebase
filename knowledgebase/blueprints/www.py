# -*- coding: utf-8 -*-

from flask import Blueprint, send_from_directory
import knowledgebase
import os


blueprint = Blueprint('web-ui', __name__)


@blueprint.route('/', defaults={'collection': None, 'resource': 'index.html'})
@blueprint.route('/index.html', defaults={'resource': None})
@blueprint.route('/<string:collection>/<path:resource>')
def static(collection, resource):
    if resource is None:
        resource, collection = collection, None

    if collection is not None:
        resource = os.path.join(collection, resource)

    root_dir = os.path.join(knowledgebase.__path__[0], 'www')
    resource_dir = os.path.dirname(resource)
    resource = os.path.basename(resource)

    return send_from_directory(
        os.path.join(root_dir, resource_dir),
        resource
    )
