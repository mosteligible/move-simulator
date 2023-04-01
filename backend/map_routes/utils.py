# database update and local distance data updater
# Update latest distance data to database
# publish latest updated distance to subscribers

# update db every 10 seconds
# publish distance update data to subscriber every 1 second

import random
import time

from message_queues.pubsub import DataSubscriber


def distance_stream(subscriber: DataSubscriber):
    """this could be any function that blocks until data is ready"""
    while True:
        yield f"data: {subscriber.receive_data()}\n\n"
