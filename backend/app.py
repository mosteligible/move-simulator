from config import AppConfig, DbConfig
from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required
from map_routes.views import route_blueprint
from models import UserModel, db
from users.views import users_blueprint
from utils import secret_key

app = Flask(AppConfig.app_name)
app.secret_key = secret_key()
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DbConfig.postgres_username}:{DbConfig.postgres_user_password}"
    f"@{DbConfig.postgres_db_host}/{DbConfig.postgres_db_name}"
)

db.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(route_blueprint, url_prefix="/routes")


# User loader
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)


@app.route("/successful_login")
@login_required
def success():
    return f"Successful Login: {current_user.username}"


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("profile_home"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
