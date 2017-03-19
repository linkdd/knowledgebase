# -*- coding: utf-8 -*-

import os


class Settings(object):
    DEBUG = bool(os.environ.setdefault(
        'KNOWLEDGEBASE_DEBUG',
        True
    ))
    TESTING = bool(os.environ.setdefault(
        'KNOWLEDGEBASE_TESTING',
        False
    ))

    DATABASE = {
        'backend': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_BACKEND',
            None
        ),
        'uri': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_URI',
            ''
        ),
        'username': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_USERNAME',
            None
        ),
        'password': os.environ.setdefault(
            'KNOWLEDGEBASE_DATABASE_PASSWORD',
            None
        )
    }

    BLUEPRINTS = [
        ('knowledgebase.blueprints.graph.blueprint', '/api/v1/graph')
    ]
