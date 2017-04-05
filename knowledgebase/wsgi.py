# -*- coding: utf-8 -*-

from knowledgebase.db.base import GraphConfig

from flask import Flask, redirect, g
from importlib import import_module
from six import raise_from
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
        try:
            graph_backend = import_module(app.config['DATABASE']['backend'])
            Graph = graph_backend.Graph

        except (ImportError, AttributeError) as err:
            raise_from(
                RuntimeError(
                    'Database backend {0} not found: {1}'.format(
                        graph_backend,
                        err
                    )
                ),
                err
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


app.config['get_database'] = get_database

# Load Flask blueprints
for blueprint, prefix in app.config['BLUEPRINTS']:
    module, attribute = blueprint.rsplit('.', 1)

    try:
        module = import_module(module)
        attribute = getattr(module, attribute)

    except (ImportError, AttributeError) as err:
        raise_from(
            RuntimeError(
                'Impossible to load blueprint {0}: {1}'.format(blueprint, err)
            ),
            err
        )

    else:
        blueprint = attribute

    app.register_blueprint(blueprint, url_prefix=prefix)

# Initialize root URL

@app.route('/')
def root_view():
    return redirect('/static/')


if __name__ == '__main__':
    from argparse import ArgumentParser
    from waitress import serve

    ap = ArgumentParser(
        description='Knowledgebase WSGI server (with waitress)'
    )
    ap.add_argument(
        '-H', '--host',
        nargs=1,
        help='Host to bind to (default: 127.0.0.1)',
        default=['127.0.0.1']
    )
    ap.add_argument(
        '-p', '--port',
        nargs=1, type=int,
        help='Port to bind to (default: 8000)',
        default=[8000]
    )

    args = ap.parse_args()

    serve(app, host=args.host[0], port=args.port[0])
