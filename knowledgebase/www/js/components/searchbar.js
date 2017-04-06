define(['component'], function(Component) {
    var SearchbarComponent = function() {
        Component.apply(this, arguments);
    };

    SearchbarComponent.prototype = Object.create(Component.prototype);

    return SearchbarComponent;
});
