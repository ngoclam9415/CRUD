from database.mysql_access.base_class.MySQLDataAccess import MySQLDataAccess
from database.search_engine.elastic_search import ElasticEngine
from database.rabbitmq_engine.client.sync_db_client import SyncDBClient

class BaseDataAccess(MySQLDataAccess, ElasticEngine, SyncDBClient):
    def __init__(self, db, model, ip="localhost", port=9200):
        MySQLDataAccess.__init__(self, db=db, model=model)
        ElasticEngine.__init__(self, ip=ip, port=port)
        SyncDBClient.__init__(self, ip="localhost", port=5673)

    def create_item(self, **kwargs):
        id = MySQLDataAccess.create_item(self, **kwargs)
        model_name = getattr(self.model, "__tablename__")
        ElasticEngine.add_to_index(self, model_name, id, kwargs)
        SyncDBClient.add_create_item(self, model_name, id, kwargs)

    def edit_item(self, id, **kwargs):
        MySQLDataAccess.edit_item(self, id, **kwargs)
        model_name = getattr(self.model, "__tablename__")
        ElasticEngine.add_to_index(self, model_name, id, kwargs)
        SyncDBClient.add_edit_item(self, model_name, id, kwargs)

    def list_item(self, **kwargs):
        pass

    def verify_qualified_item(self, **kwargs):
        return MySQLDataAccess.verify_qualified_item(self, **kwargs)
