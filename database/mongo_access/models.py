import pymongo
from config import MongoDBConfig as config
from bson.objectid import ObjectId
import math

class BaseModel:
    def __init__(self, collection="City"):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb["product"]
        self.collection = self.add_collection(collection)
        self.dict, self.list = self.get_attributes()

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
                upsert=True, new=True, fields={"_id" : 1}
        )
        if flag["_id"] not in self.dict.keys():
            kwargs["id"] = str(flag["_id"])
            self.dict[flag["_id"]] = kwargs
            self.list.append(kwargs)
        return flag

    def edit_item(self, id, **kwargs):
        object_id = ObjectId(id)
        flag = self.collection.update_one({"_id" : object_id}, {"$set" : kwargs})
        if flag.modified_count:
            print("change dict")
            self.dict[object_id].update(**kwargs)
            index = list(self.dict.keys()).index(object_id)
            self.list[index].update(**kwargs)

    def parse(self, cursors):
        dict_item = {}
        list_item = []
        for item in cursors:
            item["id"] = str(item["_id"])
            dict_item[item["_id"]] = item
            del item["_id"]
            list_item.append(item)
        return dict_item, list_item

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
    def __init__(self):
        self.city_model = BaseModel("City")
        self.district_model = BaseModel("District")
        self.brand_model = BaseModel("Brand")
        self.category_model = BaseModel("Category")
        self.address_model = BaseModel("Address")
        self.color_model = BaseModel("Color")
        self.store_model = BaseModel("Store")
        self.product_model = BaseModel("Product")
        self.product_variant_model = BaseModel("Variant")

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

db = ModelSelector()

        
if __name__ == "__main__":
    pass
