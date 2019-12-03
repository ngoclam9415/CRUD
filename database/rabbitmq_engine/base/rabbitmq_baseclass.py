import pika

class RabbitMQBaseClass:
    def __init__(self, ip="localhost", port=5673):
        params = pika.ConnectionParameters(host=ip, heartbeat=600,
                                       blocked_connection_timeout=300)
        # params.socket_timeout = 5
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

    def queue_declare(self, queue_name, durable=False):
        self.channel.queue_declare(queue_name, durable=durable)

    
