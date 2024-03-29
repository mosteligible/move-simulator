import config
from app import app
from users.models import UserModel


def initialize_consumer(user_id: str) -> None:
    """
    Initializes listeners for rabbitmq messages from devices.

    Each consumer is associated with a combination of user and device.
    For a given user and device, there will be a consumer that will
    continuously keep receiving data from device when data is sent.
    """
    with app.app_context():
        UserModel.query.all()


if __name__ == "__main__":
    app.run(host=config.AppConfig.host_ip, port=config.AppConfig.port, debug=False)
