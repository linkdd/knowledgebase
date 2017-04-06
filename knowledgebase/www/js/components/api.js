define(['component'], function(Component) {
    var APIComponent = function() {
        Component.apply(this, arguments);

        this.api_url = '/api/v1/graph';

        this.EventSystem.on('findVertices', this.findVertices, this);
        this.EventSystem.on('findEdges', this.findEdges, this);
        this.EventSystem.on('walk', this.walk, this);
    };

    APIComponent.prototype = Object.create(Component.prototype);

    APIComponent.prototype.request = function(eventName, url, method, data) {
        var me = this;

        if (method === undefined) {
            method = 'GET';
        }

        if (data === undefined) {
            data = null;
        }

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    me.EventSystem.trigger(
                        eventName + 'Result',
                        JSON.parse(xhr.responseText)
                    );
                }
                else {
                    me.EventSystem.trigger(
                        eventName + 'Failed',
                        {
                            code: xhr.status,
                            response: JSON.parse(xhr.responseText)
                        }
                    );
                }
            }
        };

        xhr.open(method, url);
        xhr.send(data);
    };

    APIComponent.prototype.buildUrl = function(endpoint, pk, params) {
        if (pk === undefined) {
            pk = null;
        }

        if (params === undefined) {
            params = null;
        }

        var url = this.api_url + '/' + endpoint;

        if (pk !== null) {
            url += '/' + pk;
        }

        if (params !== null) {
            var urlparams = '';

            for(var key in params) {
                if (urlparams !== '') {
                    urlparams += '&';
                }

                urlparams += key + '=' + encodeURIComponent(params[key]);
            }

            url += '?' + urlparams;
        }

        return url;
    };

    APIComponent.prototype.findVertices = function(event) {
        this.request('vertices', this.buildUrl('vertex', null, event.query));
    };

    APIComponent.prototype.findEdges = function(event) {
        this.request('edges', this.buildUrl('edge', null, event.query));
    };

    APIComponent.prototype.walk = function(event) {
        if (event.eid === undefined || event.query.depth === undefined) {
            this.EventSystem.trigger('invalidEvent', {
                code: 400,
                reason: 'Missing required fields'
            });
        }
        else {
            this.request(
                'walk',
                this.buildUrl('walk', event.eid, event.query)
            );
        }
    };

    return APIComponent;
});
