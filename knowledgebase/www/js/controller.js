define(['component'], function(Component) {
    var Controller = function(EventSystem, components) {
        Component.call(this, EventSystem);

        this.components = {};

        for(var key in components) {
            this.components[key] = new components[key](EventSystem);
        }
    };

    Controller.prototype = Object.create(Component.prototype);

    Controller.prototype.lookup = function(componentName) {
        return this.components[components];
    };

    return Controller;
});
