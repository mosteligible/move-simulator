# simluator-app

Simulator is a flask-based application. It uses open-street map for mapping abilities, leaflet for rendering open-street map, placing and updating markers on map. Simulator can be integrated with a data-source that emits RPM data (an arduino or a raspberry-pi with hall-effect sensor) with rabbitmq. Data from sensor is read into application, it updates recent position of the user on a designated route. Route is a path between any two points in earth that can be traversed through existing roads/paths by `routing-engine`.


