import secrets
import time
from hashlib import sha256
from random import random

import constants
from flask import request
from message_queues.pubsub import DataPublisher


def secret_key() -> str:
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key


def data_publisher(publisher: DataPublisher) -> None:
    iteration = 1
    while True:
        message = f"topic {random()/8}"
        publisher.publish_data(message)
        iteration += 1
        time.sleep(2)


def update_configs() -> None:
    return


def config_update_detector() -> None:
    """Checks update to config file and applies updated values to application."""
    prev_config_file = ""
    while True:
        time.sleep(120)
        with open(constants.config_file, "r") as fp:
            content = fp.read()
            if content != prev_config_file:
                update_configs()
                prev_config_file = content
