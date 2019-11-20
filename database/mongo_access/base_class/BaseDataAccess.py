import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from database.mongo_access.models import db

class BaseDataAccess:
    def __init__(self, db, col_name):
        self.db = db
        self.collection = self.db.add_collection(col_name)

    def create_item(self, **kwargs):
        self.collection.insert_one(kwargs)

    def edit_item(self, id, **kwargs):
        object_id = ObjectId(id)
        self.collection.update_one({"_id" : object_id}, {"$set" : kwargs})

    def list_item(self, **kwargs):
        pass

    def verify_qualified_item(self, **kwargs):
        existed_item = self.collection.find(kwargs).limit(1)
        if existed_item.count():
            return False
        return True

    def parse(self, cursors):
        dict_item = {}
        list_item = []
        print(cursors)
        for item in cursors:
            item["id"] = str(item["_id"])
            dict_item[item["_id"]] = item
            del item["_id"]
            list_item.append(item)
        return dict_item, list_item

if __name__ == "__main__":
    db = BaseDataAccess(db, "City")
    print(db.verify_qualified_item(name = "Paris"))
    # cursor = db.collection.find({})