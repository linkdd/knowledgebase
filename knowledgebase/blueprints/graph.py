# -*- coding: utf-8 -*-

from knowledgebase.forms.vertex import VertexForm
from knowledgebase.forms.edge import EdgeForm
from knowledgebase.forms.edge import WalkForm
from knowledgebase.utils import register_view

from flask import Blueprint, request, g
from flask.views import MethodView


blueprint = Blueprint('graph-api', __name__)


@register_view(blueprint, 'graph-api-edge', '/edge', pk='eid')
class EdgeView(MethodView):
    def get(self, eid):
        if eid is None:
            return {
                'success': True,
                'data': [
                    edge.data()
                    for edge in g.graph.edges.find(**request.args)
                ]
            }, 200

        else:
            edge = g.graph.edges.get(eid)

            if edge is not None:
                return {
                    'success': True,
                    'data': edge.data()
                }, 200

            else:
                return {
                    'success': False,
                    'data': None
                }, 404

    def post(self):
        form = EdgeForm(request.form)

        if form.validate():
            source = g.graph.vertices.get(form.source.data)
            target = g.graph.vertices.get(form.target.data)

            if source is None or target is None:
                return {
                    'success': False,
                    'data': None,
                    'reason': {
                        'source': source is not None,
                        'target': target is not None
                    }
                }, 400

            properties = {
                propname: request.form[propname]
                for propname in request.form
                if propname not in ['source', 'target', 'type', 'name', 'eid']
            }

            edge = g.graph.edges.create(
                source=source.eid,
                target=target.eid,
                type=form.type.data,
                name=form.name.data,
                **properties
            )
            edge.save()

            return {
                'success': True,
                'data': edge.data()
            }, 201

    def put(self, eid):
        form = EdgeForm(request.form)

        if form.validate():
            source = g.graph.vertices.get(form.source.data)
            target = g.graph.vertices.get(form.target.data)

            if source is None or target is None:
                return {
                    'success': False,
                    'data': None,
                    'reason': {
                        'source': source is not None,
                        'target': target is not None
                    }
                }, 400

            edge = g.graph.edges.get(eid)

            if edge is None:
                return {
                    'success': False,
                    'data': None
                }, 404

            edge.source = source.eid
            edge.target = target.eid
            edge.type = form.type.data
            edge.name = form.name.data

            for propname in request.form:
                if propname not in ['source', 'target', 'type', 'name', 'eid']:
                    setattr(edge, propname, request.form[propname])

            edge.save()

            return {
                'success': True,
                'data': edge.data()
            }, 200

    def delete(self, eid):
        g.graph.edges.delete(eid)

        return {
            'success': True,
            'data': None
        }, 200


@register_view(blueprint, 'graph-api-vertex', '/vertex', pk='eid')
class VertexView(MethodView):
    def get(self, eid):
        if eid is None:
            return {
                'success': True,
                'data': [
                    vertex.data()
                    for vertex in g.graph.vertices.find(**request.args)
                ]
            }, 200

        else:
            vertex = g.graph.vertices.get(eid)

            if vertex is not None:
                return {
                    'success': True,
                    'data': vertex.data()
                }, 200

            else:
                return {
                    'success': False,
                    'data': None
                }, 404

    def post(self):
        form = VertexForm(request.form)

        if form.validate():
            properties = {
                propname: request.form[propname]
                for propname in request.form
                if propname not in ['type', 'name', 'eid']
            }

            vertex = g.graph.vertices.create(
                type=form.type.data,
                name=form.name.data,
                **properties
            )
            vertex.save()

            return {
                'success': True,
                'data': vertex.data()
            }, 201

    def put(self, eid):
        form = VertexForm(request.form)

        if form.validate():
            vertex = g.graph.vertices.get(eid)

            if vertex is None:
                return {
                    'success': False,
                    'data': None
                }, 404

            vertex.type = form.type.data
            vertex.name = form.name.data

            for propname in request.form:
                if propname not in ['type', 'name', 'eid']:
                    setattr(vertex, propname, request.form[propname])

            vertex.save()

            return {
                'success': True,
                'data': vertex.data()
            }, 200

    def delete(self, eid):
        g.graph.vertices.delete(eid)

        return {
            'success': True,
            'data': None
        }, 200


@register_view(blueprint, 'graph-api-walk', '/walk', pk='eid')
class WalkView(MethodView):
    def get(self, eid):
        if eid is None:
            return {
                'success': False,
                'data': None
            }, 501

        else:
            form = WalkForm(request.args)

            if form.validate():
                depth = form.depth.data
                lookup = form.lookup.data
                match = {
                    propname: request.args[propname]
                    for propname in request.args
                    if propname not in ['depth', 'lookup']
                }

                root_vertex = g.graph.vertices.get(eid)

                if root_vertex is None:
                    return {
                        'success': False,
                        'data': None
                    }, 404

                result = {
                    'vertices': [root_vertex],
                    'edges': []
                }

                def walk(root, iteration):
                    if iteration == 0:
                        return

                    for edge in root.outE(**match):
                        if lookup in [form.LOOKUP_EDGES, form.LOOKUP_BOTH]:
                            result['edges'].append(edge)

                        vertex = edge.outV()

                        if lookup in [form.LOOKUP_VERTICES, form.LOOKUP_BOTH]:
                            result['vertices'].append(vertex)

                        walk(vertex, iteration - 1)

                walk(root_vertex, depth)

                return {
                    'success': True,
                    'data': result
                }, 200

            else:
                return {
                    'success': False,
                    'data': None,
                    'reason': form.errors
                }, 400

    def post(self):
        return {
            'success': False,
            'data': None
        }, 501

    def put(self, eid):
        return {
            'success': False,
            'data': None
        }, 501

    def delete(self, eid):
        return {
            'success': False,
            'data': None
        }, 501
