import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models import UserModel, db
from werkzeug.security import check_password_hash

from .forms import LoginForm, RegisterForm, TestForm

users_blueprint = Blueprint(
    name="users", import_name=__name__, template_folder="templates"
)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for("map_routes.routes"))
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        expected_user = UserModel.query.filter_by(username=username).first()
        if expected_user is not None and check_password_hash(
            expected_user.password, password
        ):
            login_user(expected_user)
            flash("Login Successful!")
            return redirect(url_for("map_routes.routes"))
        return "<h1> Some Validation Issues </h1>"
    return render_template("login.html", form=form)


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for("map_routes.routes"))
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = UserModel.query.filter_by(email=email).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("map_routes.routes"))

        id = str(uuid.uuid4())
        new_user = UserModel(id=id, username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("map_routes.routes"))
    return render_template("register.html", form=form)


@users_blueprint.route("/test", methods=["GET", "POST"])
def test():
    form = TestForm(request.form)
    if request.method == "POST":
        return "POST in TEST PAGE"
    return render_template("test.html", form=form)


@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
