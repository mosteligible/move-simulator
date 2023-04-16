import secrets
import time
from hashlib import sha256
from random import random

from message_queues.pubsub import DataPublisher


def secret_key() -> str:
    key = secrets.token_urlsafe()
    key = sha256(key.encode()).hexdigest()
    return key


def data_publisher(publisher: DataPublisher) -> None:
    iteration = 1
    while True:
        message = f"{random()/2}"
        publisher.publish_data(message)
        iteration += 1
        time.sleep(2)
