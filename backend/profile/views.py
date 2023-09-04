from flask import Blueprint
from flask_login import login_required

profile_blueprint = Blueprint(
    name="profile",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
)


@profile_blueprint.route("/", methods=["GET"])
@login_required
def profile():
    return "Profile Page"


@profile_blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    return "Edit profile page"
