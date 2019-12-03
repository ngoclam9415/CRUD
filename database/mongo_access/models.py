import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math
from database.redis_access.redis_accessor import RedisAccessor
import redis


class BaseLogicModel:
    def __init__(self, collection="City", redis_accessor=None):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb["product_test"]
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
            self.redis_accessor.save(kwargs["id"], kwargs)
            self.list.append(kwargs)
            self.list_id.append(str(flag["_id"]))
        return flag

    def process_sync_type(self, mongo_id, **kwargs):
        if ("mysql_id" in kwargs.keys()):
            query = {"col_type" : self.collection.name,
                            "mongo_id" : mongo_id,
                            "mysql_id" : kwargs.get("mysql_id", None)}
            self.sync_col.find_and_modify(
                    query=query,
                    update=query,
                    upsert=True, new=True
            )
            return True
        return False

    def edit_item(self, id, **kwargs):
        if id == None:
            print("id : ",id)
            mysql_id = kwargs.get("mysql_id")
            print("mysql_id : ",mysql_id)
            print("kwargs : ",kwargs)
            flag = self.collection.find_one_and_update({"mysql_id" : int(mysql_id)}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.AFTER)
            print(flag)
        else:
            object_id = ObjectId(id)
            flag = self.collection.find_one_and_update({"_id" : object_id}, {"$set" : kwargs}, return_document=pymongo.ReturnDocument.AFTER)
        if flag is not None:
            self.redis_accessor.modify(str(flag["_id"]), **kwargs)
            print(self.list_id)
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
    

    



class BaseModel(BaseLogicModel):
    def __init__(self, collection="City", redis_accessor=None, search_collection=None):
        super(BaseModel, self).__init__(collection, redis_accessor)
        self.search_collection = search_collection
    

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

redis_accessor = RedisAccessor(redis.Redis())
db = ModelSelector(redis_accessor)

        
if __name__ == "__main__":
    pass
