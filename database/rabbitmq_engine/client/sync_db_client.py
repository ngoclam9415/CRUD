import pika
from database.rabbitmq_engine.base.rabbitmq_baseclass import RabbitMQBaseClass
import json

class SyncDBClient(RabbitMQBaseClass):
    queue_name = "mysql_to_mongo"
    def __init__(self, ip="localhost", port=5673):
        super(SyncDBClient, self).__init__(ip, port)
        self.queue_declare(self.queue_name, durable=True)

    def add_to_queue(self, data):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.serialize_data(data), properties=pika.BasicProperties(
                                            delivery_mode=2,  # make message persistent
                                                ))

    def add_create_item(self, db_name, id, data):
        new_data = {"action" : "create",
                    "mysql_id" : int(id),
                    "db_name" : db_name,
                    "data" : data}
        self.add_to_queue(new_data)

    def add_edit_item(self, db_name, id, data):
        new_data = {"action" : "edit",
                    "mysql_id" : int(id),
                    "db_name" : db_name,
                    "data" : data}
        self.add_to_queue(new_data)

    def serialize_data(self, data):
        return json.dumps(data)

    
