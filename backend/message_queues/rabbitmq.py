import time
from threading import Thread

import pika
from config import brokerconfig

from .pubsub import DataPublisher


class Consumer(Thread):
    def __init__(self, user_id: str) -> None:
        self.config = brokerconfig
        self.user_id = user_id
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config.broker_host,
                port=self.config.broker_port,
                virtual_host=self.config.vhost,
                credentials=self.config.credentials,
            )
        )
        self.channel = self.connection.channel()
        self.publisher = DataPublisher(port=7777)
        self.channel.queue_declare(queue=user_id)
        self.channel.basic_consume(
            queue=self.clientId,
            on_message_callback=self.callback,
        )

    def run(self) -> str:
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body: str):
        body = body.decode("utf8")
        body = f"{self.user_id} {body}"
        self.publisher.publish_data(data=body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


class ConsumerLife:
    def __init__(self, consumer: Consumer) -> None:
        self.consumer: Consumer = consumer
        self.is_alive: bool = True
        self.last_updated: int = time.time()

    def update_checkpoint(self) -> None:
        self.last_updated = time.time()
