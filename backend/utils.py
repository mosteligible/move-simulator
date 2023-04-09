import json
import secrets
import time
from hashlib import sha256
from random import random

from config import AppConfig
from message_queues.pubsub import DataPublisher


def secret_key() -> str:
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key


def data_publisher(publisher: DataPublisher) -> None:
    iteration = 1
    while True:
        sleep_time = random()
        if sleep_time > 0.6:
            sleep_time = 1
        message = json.dumps({"iteration": iteration})
        publisher.publish_data(message)
        iteration += 1
        time.sleep(sleep_time)
