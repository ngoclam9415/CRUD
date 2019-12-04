import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis
from database.mongo_access.base_class.BaseLogicModel import BaseLogicModel
from database.mongo_access.base_class.BaseModel import BaseModel

class ModelSelector:
    def __init__(self, redis_accessor):
        self.search_model = BaseLogicModel("Search", redis_accessor)
        self.search_model.create_indexes()
        self.city_model = BaseModel("City", redis_accessor, self.search_model.collection)
        self.district_model = BaseModel("District", redis_accessor, self.search_model.collection)
        self.brand_model = BaseModel("Brand", redis_accessor, self.search_model.collection)
        self.category_model = BaseModel("Category", redis_accessor, self.search_model.collection)
        self.address_model = BaseModel("Address", redis_accessor, self.search_model.collection)
        self.color_model = BaseModel("Color", redis_accessor, self.search_model.collection)
        self.store_model = BaseModel("Store", redis_accessor, self.search_model.collection)
        self.product_model = BaseModel("Product", redis_accessor, self.search_model.collection)
        self.product_variant_model = BaseModel("Variant", redis_accessor, self.search_model.collection)
        self.redis_accessor = redis_accessor

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
        elif model_type == "Search":
            return self.search_model
            
    def init_app(self, app):
        print("HELLO APP")

    def drop_all(self):
        self.search_model.db.drop_collection("City")
        self.search_model.db.drop_collection("District")
        self.search_model.db.drop_collection("Address")
        self.search_model.db.drop_collection("Store")
        self.search_model.db.drop_collection("Brand")
        self.search_model.db.drop_collection("Category")
        self.search_model.db.drop_collection("Product")
        self.search_model.db.drop_collection("Color")
        self.search_model.db.drop_collection("Variant")
        self.search_model.db.drop_collection("Search")
        self.search_model.db.drop_collection("Sync")

    def create_all(self):
        self.__init__(self.redis_accessor)

redis_accessor = RedisAccessor(redis.Redis())
db = ModelSelector(redis_accessor)

        
if __name__ == "__main__":
    pass
