from database.mysql_access.base_class.MySQLDataAccess import MySQLDataAccess
from database.search_engine.elastic_search import ElasticEngine

class BaseDataAccess(MySQLDataAccess, ElasticEngine):
    def __init__(self, db, model, ip="localhost", port=9200):
        MySQLDataAccess.__init__(self, db=db, model=model)
        ElasticEngine.__init__(self, ip=ip, port=port)

    def create_item(self, **kwargs):
        id = super(BaseDataAccess, self).create_item(**kwargs)
        model_name = getattr(self.model, "__tablename__")
        super(BaseDataAccess, self).add_to_index(model_name, id, kwargs)

    def edit_item(self, id, **kwargs):
        super(BaseDataAccess, self).edit_item(id, **kwargs)
        model_name = getattr(self.model, "__tablename__")
        super(BaseDataAccess, self).add_to_index(model_name, id, kwargs)

    def list_item(self, **kwargs):
        pass

    def verify_qualified_item(self, **kwargs):
        return super(BaseDataAccess, self).verify_qualified_item(**kwargs)
