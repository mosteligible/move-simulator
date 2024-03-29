import secrets
import time
from hashlib import sha256
from random import random
from typing import Dict

import constants
from message_queues.pubsub import DataPublisher
from message_queues.rabbitmq import ConsumerLife

CONSUMERS: Dict[str, ConsumerLife] = {}


def secret_key() -> str:
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key


def data_publisher(publisher: DataPublisher) -> None:
    iteration = 1
    while True:
        message = f"{random()/8}"
        publisher.publish_data(message)
        iteration += 1
        time.sleep(2)


def update_configs() -> None:
    return


def thread_life_handler() -> None:
    ...


def config_update_detector() -> None:
    """Checks update to config file and applies updated values to application."""
    prev_config_file = ""
    while True:
        time.sleep(120)
        with open(constants.CONFIG_FILE_PATH, "r") as fp:
            content = fp.read()
            if content != prev_config_file:
                update_configs()
                prev_config_file = content
