define(['lib/vivagraph', 'component'], function(Viva, Component) {
    var GraphComponent = function() {
        Component.apply(this, arguments);

        this.container = document.getElementById('graph-component-container');
        this.graph = Viva.Graph.graph();
        this.EventSystem.on('walkResult', this.populateGraph, this);
    };

    GraphComponent.prototype = Object.create(Component.prototype);

    GraphComponent.prototype.populateGraph = function(result) {
        var i, l;

        for(i = 0, l = result.data.vertices.length; i < l; i++) {
            var vertex = result.data.vertices[i];
            this.graph.addNode(vertex.eid, vertex);
        }

        for(i = 0, l = result.data.edges.length; i < l; i++) {
            var edge = result.data.edges[i];
            this.graph.addLink(edge.source.eid, edge.target.eid);
        }

        this.render();
    };

    GraphComponent.prototype.render = function() {
        var renderer = Viva.Graph.View.renderer(this.graph, {
            container: this.container
        });
        renderer.run();
    };

    return GraphComponent;
});
