# -*- coding: utf-8 -*-

from knowledgebase.db.base import GraphConfig

from b3j0f.utils.path import lookup
from flask import Flask, g
import os


# Initialize and configure WSGI application
app = Flask(__name__)
app.config.from_object(
    os.environ.setdefault(
        'KNOWLEDGEBASE_SETTINGS',
        'knowledgebase.settings.base.Settings'
    )
)


def get_database():
    db = getattr(g, 'graph', None)

    if db is None:
        # Check for database configuration
        if app.config['DATABASE'].get('backend') is None:
            raise RuntimeError('No database configured')

        # Try to load database backend
        graph_backend = app.config['DATABASE']['backend']

        try:
            Graph = lookup('{0}.Graph'.format(graph_backend))

        except ImportError:
            raise RuntimeError(
                'Database backend not found: {0}'.format(graph_backend)
            )

        # Initialize and configure database
        graphcfg = GraphConfig(
            uri=app.config['DATABASE'].get('uri', ''),
            username=app.config['DATABASE'].get('username'),
            password=app.config['DATABASE'].get('password')
        )

        g.graph = Graph(conf=graphcfg)

    return g.graph


@app.teardown_appcontext
def close_database(error):
    db = getattr(g, 'graph', None)

    if db is not None:
        db.close()


# Load Flask blueprints
for blueprint, prefix in app.config['BLUEPRINTS']:
    blueprint = lookup(blueprint)
    app.register_blueprint(blueprint, url_prefix=prefix)
