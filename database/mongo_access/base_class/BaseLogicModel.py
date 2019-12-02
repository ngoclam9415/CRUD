import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis


class BaseLogicModel:
    def __init__(self, collection="City", redis_accessor=None):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb["product"]
        self.collection = self.add_collection(collection)
        self.redis_accessor = redis_accessor
        self.list_id, self.list = self.get_attributes()

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
        if self.redis_accessor is not None and not self.redis_accessor.exist(str(flag["_id"])) :
            kwargs["id"] = str(flag["_id"])
            self.redis_accessor.save(kwargs["id"], kwargs)
            self.list.append(kwargs)
        return flag

    def edit_item(self, id, **kwargs):
        object_id = ObjectId(id)
        flag = self.collection.find_one_and_update({"_id" : object_id}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.AFTER)
        if flag is not None:
            if self.redis_accessor is not None:
                self.redis_accessor.modify(id, **kwargs)
            index = self.list_id.index(id)
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