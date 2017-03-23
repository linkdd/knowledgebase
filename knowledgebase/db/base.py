# -*- coding: utf-8 -*-

from copy import deepcopy


class GraphConfig(object):
    def __init__(
        self,
        uri=None,
        username=None,
        password=None,
        *args, **kwargs
    ):
        super(GraphConfig, self).__init__(*args, **kwargs)

        self._uri = uri
        self._username = username
        self._password = password

    @property
    def uri(self):
        return self._uri

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


class Element(object):
    def __init__(self, graph, data=None, *args, **kwargs):
        super(Element, self).__init__(*args, **kwargs)

        self._graph = graph
        self._data = {}

        if data is not None:
            self._data = deepcopy(data)

    def __getattr__(self, attr):
        return self.__dict__['_data'].get(attr)

    def __setattr__(self, attr, val):
        if attr not in ['_data', '_graph']:
            self._data[attr] = val

        else:
            super(Element, self).__setattr__(attr, val)

    def __delattr__(self, attr):
        if attr not in ['_data', '_graph']:
            self._data.pop(attr)

        else:
            super(Element, self).__delattr__(attr)

    @classmethod
    def get(cls, graph, eid):
        raise NotImplementedError('Abstract class cannot get element')

    @classmethod
    def get_all(cls, graph):
        raise NotImplementedError('Abstract class cannot get all elements')

    def save(self):
        raise NotImplementedError('Abstract class cannot save element')

    def data(self):
        return deepcopy(self._data)


class Vertex(Element):
    def outE(self, **properties):
        raise NotImplementedError('Abstract class cannot get outgoing edges')

    def inE(self, **properties):
        raise NotImplementedError('Abstract class cannot get incomming edges')

    def bothE(self, **properties):
        raise NotImplementedError('Abstract class cannot get edges')

    def outV(self, **properties):
        for edge in self.outE(**properties):
            yield edge.outV()

    def inV(self, **properties):
        for edge in self.inE(**properties):
            yield edge.inV()

    def bothV(self, **properties):
        for edge in self.bothE(**properties):
            for vertex in edge.bothV():
                if vertex.eid != self.eid:
                    yield vertex


class Edge(Element):
    def outV(self):
        raise NotImplementedError('Abstract class cannot get outgoing vertex')

    def inV(self):
        raise NotImplementedError('Abstract class cannot get incomming vertex')

    def bothV(self):
        raise NotImplementedError('Abstract class cannot get vertices')


class ElementView(object):
    def __init__(self, graph, cls, *args, **kwargs):
        super(ElementView, self).__init__(*args, **kwargs)

        self.graph = graph
        self.cls = cls

    def create(self, **kwargs):
        elt = self.cls(self.graph, data=kwargs)
        return elt

    def get(self, eid):
        return self.cls.get(self.graph, eid)

    def get_all(self):
        return self.cls.get_all(self.graph)

    def find(self, **properties):
        raise NotImplementedError('Abstract class cannot find elements')

    def update(self, eid, **data):
        raise NotImplementedError('Abstract class cannot update element')

    def delete(self, eid):
        raise NotImplementedError('Abstract class cannot delete element')


class Graph(object):

    elementview_class = ElementView
    vertex_class = Vertex
    edge_class = Edge

    def __init__(self, conf=None, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)

        if conf is None:
            conf = GraphConfig()

        self._conf = conf
        self._vertices = self.elementview_class(self, self.vertex_class)
        self._edges = self.elementview_class(self, self.edge_class)

    @property
    def conf(self):
        return self._conf

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def close(self):
        raise NotImplementedError('Abstract class cannot close database')
