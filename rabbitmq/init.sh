#!/bin/sh

# Create Rabbitmq user
echo "default_user = $DEFAULT_USER
default_pass = $DEFAULT_USER_PLAIN_PASSWORD

listeners.tcp.default = $LISTENER_PORT

management.tcp.port = $MANAGEMENT_TCP_PORT

management.load_definitions = /etc/rabbitmq/definitions.json
" > ./rabbitmq/rabbitmq.conf
