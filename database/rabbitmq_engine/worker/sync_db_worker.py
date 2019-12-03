import pika
from database.rabbitmq_engine.base.rabbitmq_baseclass import RabbitMQBaseClass
import json
from app import access_factory

class SyncDBWorker(RabbitMQBaseClass):
    queue_name = "mysql_to_mongo"
    def __init__(self, ip="localhost", port=5673):
        super(SyncDBWorker, self).__init__(ip, port)
        self.queue_declare(self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.queue_name, on_message_callback=self.synchronize_data)
        self.channel.start_consuming()

    def synchronize_data(self, ch, method, properties, body):
        data = self.deserialize_data(body)
        if data["action"] == "create":
            self.sync_created_item(data)
        elif data["action"] == "edit":
            self.sync_edited_data(data)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def sync_created_item(self, data):
        data["data"]["mysql_id"] = data["mysql_id"]
        access_factory.get_access(data["db_name"]).create_item(**data["data"])

    def sync_edited_data(self, data):
        data["data"]["mysql_id"] = data["mysql_id"]
        access_factory.get_access(data["db_name"]).edit_item(None, **data["data"])
    
    def deserialize_data(self, data):
        return json.loads(data)


    
if __name__ == "__main__":
    worker = SyncDBWorker()