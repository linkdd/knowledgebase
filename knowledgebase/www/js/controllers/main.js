define(['controller'], function(Controller) {
    var MainController = function() {
        Controller.apply(this, arguments);

        this.checkRootVertexId = this.EventSystem.on(
            'verticesResult',
            this.checkRootVertex,
            this
        );
        this.EventSystem.trigger('findVertices', {
            query: {
                type: 'root'
            }
        });
    };

    MainController.prototype = Object.create(Controller.prototype);

    MainController.prototype.checkRootVertex = function(response) {
        if (response.data.length === 0) {
            console.error('No root vertex found!');
        }
        else {
            var vertex = response.data[0];

            this.EventSystem.trigger('walk', {
                eid: vertex.eid,
                query: {
                    depth: 3
                }
            });
            this.EventSystem.off(this.checkRootVertexId);
            this.checkRootVertexId = null;
        }
    };

    return MainController;
});
