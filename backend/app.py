from threading import Thread

from config import AppConfig, DbConfig
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from map_routes.views import route_blueprint
from message_queues.pubsub import DataPublisher
from models import UserModel, db
from users.views import users_blueprint
from utils import data_publisher, secret_key

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


@app.route("/")
def index():
    return redirect(url_for("users.login"))


@app.route("/status")
def status():
    return {"status": 200}


if __name__ == "__main__":
    publisher = DataPublisher()
    data_generator_thread = Thread(
        target=data_publisher, args=(publisher,), daemon=True
    )
    data_generator_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
