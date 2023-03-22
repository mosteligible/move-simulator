import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from models import UserModel, db
from werkzeug.security import check_password_hash

from .forms import LoginForm, RegisterForm

users_blueprint = Blueprint(name="users", import_name=__name__, template_folder="templates")


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        expected_user = UserModel.query.filter_by(username=username).first()
        if expected_user is not None and check_password_hash(
            expected_user.password, password
        ):
            login_user(expected_user)
            flash("Login Successful!")
            return "<h3> Successful Login! </h3>"
        return "<h1> Some Validation Issues </h1>"
    return render_template("login.html", form=form)


@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = UserModel.query.filter_by(email=email).first()
        if user is not None:
            return redirect(url_for("/"))

        id = str(uuid.uuid4())
        new_user = UserModel(id=id, username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        return "Successful Registration!"
    return render_template("register.html", form=form)
