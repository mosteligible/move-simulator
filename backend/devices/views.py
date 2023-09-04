from flask import Blueprint
from flask_login import login_required

devices_blueprint = Blueprint(
    name="devices",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)


@devices_blueprint.route("/", methods=["GET"])
@login_required
def devices():
    return "Devices Page"


@devices_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_device():
    return "Add device page"
