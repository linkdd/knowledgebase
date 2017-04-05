# -*- coding: utf-8 -*-

import os


class Settings(object):
    DEBUG = bool(os.environ.setdefault(
        'KNOWLEDGEBASE_DEBUG',
        '1'
    ))
    TESTING = bool(os.environ.setdefault(
        'KNOWLEDGEBASE_TESTING',
        '0'
    ))

    DATABASE = {
        'backend': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_BACKEND',
            ''
        ),
        'uri': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_URI',
            ''
        ),
        'username': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_USERNAME',
            ''
        ),
        'password': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_PASSWORD',
            ''
        )
    }

    BLUEPRINTS = [
        ('knowledgebase.blueprints.graph.blueprint', '/api/v1/graph'),
        ('knowledgebase.blueprints.www.blueprint', '/static')
    ]

    ROOT_REDIRECT = '/static/index.html'
