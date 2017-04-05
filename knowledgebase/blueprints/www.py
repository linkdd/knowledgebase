# -*- coding: utf-8 -*-

from flask import Blueprint, send_from_directory
import knowledgebase
import os


blueprint = Blueprint('web-ui', __name__)


@blueprint.route('/', defaults={'path': 'index.html'})
@blueprint.route('/<path:path>')
def static(path):
    if path is None:
        path = 'index.html'

    return send_from_directory(
        os.path.join(knowledgebase.__path__[0], 'www'),
        path
    )
