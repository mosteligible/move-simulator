from config import AppConfig, DbConfig
from flask import Flask
from flask_login import LoginManager
from models import UserModel, db
from users.views import users_blueprint
from utils import secret_key

app = Flask(AppConfig.app_name)
app.secret_key = secret_key()
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DbConfig.mysql_username}:{DbConfig.mysql_user_password}"
    f"@{DbConfig.mysql_db_host}/{DbConfig.mysql_db_name}"
)

db.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(users_blueprint)


# User loader
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)


@app.route("/")
def index():
    return "<h1>Home Page</h1>"


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
