define(function() {
    var EventSystem = function() {
        this._eventHandlers = {};
        this._nbHandlers = 0;
    };

    EventSystem.prototype = {
        ready: function(fn, context) {
            if (context === undefined) {
                context = this;
            }

            if (document.readyState === 'complete') {
                fn.call(context);
            }
            else {
                document.addEventListener('DOMContentLoaded', function() {
                    fn.call(context);
                });
            }
        },
        on: function(eventName, eventHandler, context, target) {
            if (context === undefined) {
                context = this;
            }

            if (target === undefined) {
                target = document;
            }

            var eventId = this._nbHandlers;
            var event = {
                name: eventName,
                target: target,
                handler: function() {
                    return eventHandler.apply(context, arguments);
                }
            };

            this._eventHandlers[eventId] = event;
            this._nbHandlers++;

            target.addEventListener(event.name, event.handler);
            return eventId;
        },
        off: function(eventId) {
            var event = this._eventHandlers[eventId];

            if (event !== undefined) {
                event.target.removeEventListener(event.name, event.handler);
                delete this._eventHandlers[eventId];
            }
        },
        trigger: function(eventName, eventData) {
            var event = new CustomEvent(eventName, eventData);
            document.dispatchEvent(event);
        }
    };

    return EventSystem;
});
