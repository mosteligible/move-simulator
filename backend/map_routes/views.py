import uuid

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from message_queues.pubsub import DataSubscriber
from models import db

from .forms import RouteAddForm
from .models import Route
from .utils import distance_stream, get_coordinates_from_address, get_route_coordinates

route_blueprint = Blueprint(
    name="map_routes",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)


@route_blueprint.route("/", methods=["GET", "POST"])
@login_required
def routes():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    userid = current_user.id
    routes = Route.query.filter_by(userid=userid).all()
    return render_template("route.html", user_added_routes=routes)


@route_blueprint.route("/add_route", methods=["GET", "POST"])
# @login_required
def add_route():
    routeaddform = RouteAddForm(request.form)
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))
    cur_usr = current_user
    username = cur_usr.username
    user_id = cur_usr.id
    message = ""
    if request.method == "POST" and routeaddform.validate():
        # send request to nominatim app
        start_street_address = routeaddform.start_street_address.data
        start_city_name = routeaddform.start_city_name.data
        start_country_name = routeaddform.start_country_name.data
        start_postal_code = routeaddform.start_postal_code.data
        stop_street_address = routeaddform.stop_street_address.data
        stop_city_name = routeaddform.stop_city_name.data
        stop_country_name = routeaddform.stop_country_name.data
        stop_postal_code = routeaddform.stop_postal_code.data

        start_geocode_data = get_coordinates_from_address(
            street_address=start_street_address,
            city_name=start_city_name,
            country_name=start_country_name,
            postal_code=start_postal_code,
        )
        stop_geocode_data = get_coordinates_from_address(
            street_address=stop_street_address,
            city_name=stop_city_name,
            country_name=stop_country_name,
            postal_code=stop_postal_code,
        )
        if start_geocode_data is False or stop_geocode_data is False:
            invalid_point = (
                start_street_address
                if start_geocode_data is False
                else stop_street_address
            )
            message = f"Invalid address for {invalid_point} point."
            return render_template("route_add.html", form=routeaddform, message=message)
        start_to_stop_route_coordinates = get_route_coordinates(
            start_coordinate=start_geocode_data, stop_coordinate=stop_geocode_data
        )
        if start_to_stop_route_coordinates is False:
            message = (
                "Error! Either start or stop address is out of scope for routing."
                " Please select one within Ontario!"
            )
            return render_template("route_add.html", form=routeaddform, message=message)
        route = Route(
            id=str(uuid.uuid4()),
            username=username,
            userid=user_id,
            distance_covered=0,
            last_position=start_geocode_data,
            start_street_address=start_street_address,
            start_city=start_city_name,
            start_country=start_country_name,
            end_street_address=stop_street_address,
            end_city=stop_city_name,
            end_country=stop_country_name,
            start_position=start_geocode_data,
            end_position=stop_geocode_data,
            route_coordinates=start_to_stop_route_coordinates,
        )
        db.session.add(route)
        db.session.commit()
        message = f"{start_geocode_data}, {stop_geocode_data}"
        flash("Route Added Successfully!")
        return redirect(url_for("map_routes.routes"))

    message = "get_form"
    return render_template("route_add.html", form=routeaddform, message=message)


@route_blueprint.route("/stream")
@login_required
def stream():
    subscriber = DataSubscriber(host="localhost")
    return Response(
        distance_stream(subscriber=subscriber), mimetype="text/event-stream"
    )


@route_blueprint.route("/simulate")
def simulate():
    return render_template("route_simluator.html")


global i
i = 0


@route_blueprint.route("/running/<route_id>", methods=["GET"])
@login_required
def running(route_id):
    global i
    print(f"-- Route ID: {route_id}, i; {i}")
    i += 1
    route_data = Route.query.filter_by(id=route_id).first()
    print("-- type(route_data.route_coordinates)", type(route_data.route_coordinates))
    coordinates = route_data.route_coordinates["coordinates"]
    return render_template("route_runner.html", routejson=coordinates)


@route_blueprint.route("/hard")
def test():
    return render_template("hardcoded.html")
