from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models import UserModel, db
from .forms import RouteAddForm


route_blueprint = Blueprint(
    name="map_routes",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)


@route_blueprint.route("/", methods=["GET", "POST"])
@login_required
def routes():
    users = UserModel.query
    return render_template("route.html", user_added_routes=users)


@route_blueprint.route("/add_route", methods=["GET", "POST"])
@login_required
def add_route():
    form = RouteAddForm(request.form)
    return render_template("route_add.html", form=form)
