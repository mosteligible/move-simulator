import pika
from config import brokerconfig

from .pubsub import DataPublisher


class Consumer:
    def __init__(self, clientId: str) -> None:
        self.config = brokerconfig
        self.clientId = clientId
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
        self.channel.queue_declare(queue=clientId)
        self.channel.basic_consume(
            queue=self.clientId,
            on_message_callback=self.callback,
        )

    def run(self) -> str:
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body: str):
        body = body.decode("utf8")
        self.publisher.publish_data(data=body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
