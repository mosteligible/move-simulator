import zmq


class DataPublisher:
    def __init__(self, port: int = 7777) -> None:
        self.port = port
        self.connection_string = f"tcp://*:{port}"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.connection_string)

    def publish_data(self, data: str) -> str:
        self.socket.send_string(data)


class DataSubscriber:
    def __init__(self, user_id: str, host: str, port: int = 7777) -> None:
        self.port = port
        self.host = host
        self.user_id = user_id
        self.connection_string = f"tcp://{host}:{port}"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(self.connection_string)
        self.socket.subscribe("")

    def receive_data(self) -> str:
        return self.socket.recv_string()
