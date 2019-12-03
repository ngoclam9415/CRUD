import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis
from database.mongo_access.base_class.BaseLogicModel import BaseLogicModel

class BaseModel(BaseLogicModel):
    def __init__(self, collection="City", redis_accessor=None, search_collection=None):
        super(BaseModel, self).__init__(collection, redis_accessor)
        self.search_collection = search_collection
    
    def parse(self, cursors):
        list_id = []
        list_item = []
        for item in cursors:
            item["id"] = str(item["_id"])
            item["type"] = self.collection.name.lower()
            list_id.append(item["id"])
            del item["_id"]
            if self.redis_accessor is not None:
                self.redis_accessor.save(item["id"], item)
            # self.queue_client.create_item(item)
            list_item.append(item)
        return list_id, list_item

    def create_search_item(self, **kwargs):
        length = len(list(kwargs.keys()))
        kwargs["len"] = length
        flag = self.search_collection.find_and_modify(
                query=kwargs,
                update=kwargs,
                upsert=True, new=True
        )
        return flag

    def edit_search_item(self, id, **kwargs):
        flag = self.search_collection.find_one_and_update({"id" : id}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.BEFORE)
        if flag is not None:
            self.redis_accessor.modify(id, **kwargs)
            index = self.list_id.index(id)
            self.list[index].update(**kwargs)

            flag = dict(flag)
            old_fields = {}
            update_fields = {}
            for key, value in kwargs.items():
                old_value = flag.get(key, None)
                if old_value is not None and old_value != value and key not in ["_id", "id", "type"]:
                    update_fields[key] = value
                    old_fields[key] = old_value
            if "len" in flag.keys():
                old_fields["len"] = {"$gt" : flag["len"]}
            if update_fields:
                self.search_collection.update_many(old_fields,
                                                    {"$set" : update_fields})
        return flag