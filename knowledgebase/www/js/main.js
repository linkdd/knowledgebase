requirejs.config({
    'baseUrl': 'js'
});

define([
    'events',
    'components/graph',
    'components/searchbar',
    'components/api',
    'controllers/main'
], function(
    EventSystem,
    GraphComponent,
    SearchbarComponent,
    APIComponent,
    MainController
) {
    var EventSystem = new EventSystem();

    EventSystem.ready(function() {
        var MainController = new MainController(EventSystem, {
            graph: GraphComponent,
            searchbar: SearchbarComponent,
            api: APIComponent
        });

        window.MainController = MainController;
    });

    window.EventSystem = EventSystem;
});
