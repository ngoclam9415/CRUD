import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis
import os


class BaseLogicModel:
    def __init__(self, collection="City", redis_accessor=None):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb[os.getenv("TEST_DB") or "product_test"]
        self.collection = self.add_collection(collection)
        self.redis_accessor = redis_accessor
        self.list_id, self.list = self.get_attributes()
        self.sync_col = self.add_collection("Sync")

    def get_attributes(self):
        cursors = self.collection.find({})
        cursors = list(cursors)
        return self.parse(cursors)

    def add_collection(self, col_name):
        return self.db[col_name]

    def create_item(self, **kwargs):
        flag = self.collection.find_and_modify(
                query=kwargs,
                update=kwargs,
                upsert=True, new=True
        )

        self.process_sync_type(str(flag["_id"]), **kwargs)

        if not self.redis_accessor.exist(str(flag["_id"])):
            kwargs["id"] = str(flag["_id"])
            if self.redis_accessor is not None:
                self.redis_accessor.save(kwargs["id"], kwargs)
            self.list.append(kwargs)
            self.list_id.append(str(flag["_id"]))
        else:
            print("Duplicate key in redis")
            kwargs["id"] = str(flag["_id"])
            if self.redis_accessor is not None:
                self.redis_accessor.save(kwargs["id"], kwargs)
            self.list.append(kwargs)
            self.list_id.append(str(flag["_id"]))
        return flag

    def process_sync_type(self, mongo_id, **kwargs):
        if ("mysql_id" in kwargs.keys()):
            query = {"col_type" : self.collection.name,
                            "mongo_id" : mongo_id,
                            "mysql_id" : kwargs.get("mysql_id", None)}
            data = self.sync_col.find_and_modify(
                    query=query,
                    update=query,
                    upsert=True, new=True
            )
            return True
        return False

    def edit_item(self, id, **kwargs):
        if id == None:
            mysql_id = kwargs.get("mysql_id")
            flag = self.collection.find_one_and_update({"mysql_id" : int(mysql_id)}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.AFTER)
        else:
            object_id = ObjectId(id)
            flag = self.collection.find_one_and_update({"_id" : object_id}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.AFTER)
        if flag is not None:
            if self.redis_accessor is not None:
                self.redis_accessor.modify(str(flag["_id"]), **kwargs)
            index = self.list_id.index(str(flag["_id"]))
            self.list[index].update(**kwargs)
        return flag

    def parse(self, cursors):
        list_id = []
        list_item = []
        for item in cursors:
            item["id"] = str(item["_id"])
            list_id.append(item["id"])
            del item["_id"]
            if self.redis_accessor is not None:
                self.redis_accessor.save(item["id"], item)
            list_item.append(item)
        return list_id, list_item

    def verify_qualified_item(self, **kwargs):
        existed_item = self.collection.find(kwargs).limit(1)
        if existed_item.count():
            return False
        return True

    def paginate(self, page, perpage):
        start = page*perpage - perpage
        return self.list[start:start+perpage]

    def get_pages(self, per_page):
        return max(math.ceil(len(self.list)/per_page), 1)

    def create_indexes(self):
        self.collection.create_index([("$**", pymongo.TEXT)])

    def show_searched_item(self, text):
        cursors = self.collection.aggregate([
                                    {"$match" : {"$text" : {"$search" : text}}},
                                    {"$group" : {"_id" : "$type", "data" : {"$push" : "$$ROOT"}}},
                                    ])
        return_dict = {}
        for cursor in cursors:
            return_dict[cursor["_id"]] = cursor["data"]
        return return_dict