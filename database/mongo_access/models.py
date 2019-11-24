import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis


class BaseModel:
    def __init__(self, collection="City", redis_accessor=None):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb["product"]
        self.collection = self.add_collection(collection)
        self.redis_accessor = redis_accessor
        self.list_key, self.list = self.get_attributes()

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
        if not self.redis_accessor.exist(str(flag["_id"])):
            kwargs["id"] = str(flag["_id"])
            self.redis_accessor.save(kwargs["id"], kwargs)
            self.list.append(kwargs)
        return flag

    def edit_item(self, id, **kwargs):
        object_id = ObjectId(id)
        flag = self.collection.update_one({"_id" : object_id}, {"$set" : kwargs})
        if flag.modified_count:
            self.redis_accessor.modify(id, **kwargs)
            index = self.list_key.index(id)
            self.list[index].update(**kwargs)

    def parse(self, cursors):
        list_key = []
        list_item = []
        for item in cursors:
            item["id"] = str(item["_id"])
            list_key.append(item["id"])
            del item["_id"]
            self.redis_accessor.save(item["id"], item)
            list_item.append(item)
        return list_key, list_item

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

    

class ModelSelector:
    def __init__(self, redis_accessor):
        self.city_model = BaseModel("City", redis_accessor)
        self.district_model = BaseModel("District", redis_accessor)
        self.brand_model = BaseModel("Brand", redis_accessor)
        self.category_model = BaseModel("Category", redis_accessor)
        self.address_model = BaseModel("Address", redis_accessor)
        self.color_model = BaseModel("Color", redis_accessor)
        self.store_model = BaseModel("Store", redis_accessor)
        self.product_model = BaseModel("Product", redis_accessor)
        self.product_variant_model = BaseModel("Variant", redis_accessor)

    def select(self, model_type):
        if model_type == "City":
            return self.city_model
        elif model_type == "District":
            return self.district_model
        elif model_type == "Brand":
            return self.brand_model
        elif model_type == "Category":
            return self.category_model
        elif model_type == "Address":
            return self.address_model
        elif model_type == "Color":
            return self.color_model
        elif model_type == "Store":
            return self.store_model
        elif model_type == "Product":
            return self.product_model
        elif model_type == "Variant":
            return self.product_variant_model
            
    def init_app(self, app):
        print("HELLO APP")

redis_accessor = RedisAccessor(redis.Redis())
db = ModelSelector(redis_accessor)

        
if __name__ == "__main__":
    pass
