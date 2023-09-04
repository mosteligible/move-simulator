from threading import Thread

import utils
from app import app
from config import AppConfig
from users.models import UserModel


def initialize_consumers() -> None:
    """
    Initializes listeners for rabbitmq messages from devices.

    Each consumer is associated with a combination of user and device.
    For a given user and device, there will be a consumer that will
    continuously keep receiving data from device when data is sent.
    """
    with app.app_context():
        users = UserModel.query.all()


if __name__ == "__main__":
    config_thread = Thread(target=utils.config_update_detector, daemon=True)
    config_thread.start()
    app.run(host=AppConfig.host_ip, port=AppConfig.port, debug=False)
