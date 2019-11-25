import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

class BaseDataAccess:
    def __init__(self, db, col_name):
        self.db = db
        self.collection = self.db.select(col_name)

    def create_item(self, **kwargs):
        result = self.collection.create_item(**kwargs)
        if result is not None:
            return dict(result)
        return result

    def edit_item(self, id, **kwargs):
        result = self.collection.edit_item(id, **kwargs)
        if result is not None:
            return dict(result)
        return result

    def list_item(self, **kwargs):
        pass

    def verify_qualified_item(self, **kwargs):
        return self.collection.verify_qualified_item(**kwargs)


if __name__ == "__main__":
    db = BaseDataAccess(db, "City")
    print(db.verify_qualified_item(name = "Paris"))
    # cursor = db.collection.find({})