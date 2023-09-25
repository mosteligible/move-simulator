import uuid

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    session,
    stream_with_context,
    url_for,
)
from flask_login import current_user, login_required
from message_queues.pubsub import DataSubscriber
from models import db

from .forms import RouteAddForm
from .map_helpers import Position, RouteHelper
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
    user_id = current_user.id
    routes = Route.query.filter_by(userid=user_id).all()
    return render_template("route.html", user_added_routes=routes)


@route_blueprint.route("/add_route", methods=["GET", "POST"])
@login_required
def add_route():
    routeaddform = RouteAddForm(request.form)
    cur_usr = current_user
    username = cur_usr.username
    user_id = cur_usr.id
    message = ""
    if request.method == "POST" and routeaddform.validate():
        # send request to reverse-geocoder
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

        # Get route coordinates from routing-engine
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
            total_distance_covered=0,
            last_position_index=0,
            start_street_address=start_street_address,
            start_city=start_city_name,
            start_country=start_country_name,
            end_street_address=stop_street_address,
            end_city=stop_city_name,
            end_country=stop_country_name,
            start_position=start_geocode_data,
            end_position=stop_geocode_data,
            route_coordinates=start_to_stop_route_coordinates,
            num_route_coordinates=len(start_to_stop_route_coordinates),
        )
        db.session.add(route)
        db.session.commit()
        message = f"{start_geocode_data}, {stop_geocode_data}"
        flash("Route Added Successfully!")
        return redirect(url_for("map_routes.routes"))

    message = "get_form"
    return render_template("route_add.html", form=routeaddform, message=message)


@route_blueprint.route("/stream/<route_id>")
@login_required
def stream(route_id: str):
    user_id = current_user.id
    subscriber = DataSubscriber(user_id=user_id, host="localhost")
    route = Route.query.filter_by(id=route_id).first()
    return Response(
        stream_with_context(distance_stream(subscriber=subscriber, route=route)),
        mimetype="text/event-stream",
    )


@route_blueprint.route("/running/<route_id>", methods=["GET"])
@login_required
def running(route_id: str):
    route_data = Route.query.filter_by(id=route_id).first()
    route_proxy = RouteHelper(route=route_data)
    start_position = Position(
        street_address=route_proxy.start_street_address,
        coordinates=route_proxy.start_position,
    )
    end_position = Position(
        street_address=route_proxy.end_street_address,
        coordinates=route_proxy.end_position,
    )
    return render_template(
        "route_runner.html",
        route_data=route_proxy,
        start_position=start_position,
        end_position=end_position,
    )


@route_blueprint.route("/is_running", methods=["POST"])
@login_required
def is_running():
    data = request.data
