from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json
import math

class CategoryDataAccess(BaseDataAccess):
    def __init__(self, db, category_model, brand_col):
        super(CategoryDataAccess, self).__init__(db, category_model)
        self.brand_col = db.add_collection(brand_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        brands = self.query_brands()
        categories = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        brands_dict, brands_list = self.parse(brands)
        categories = list(categories)
        categories = self.create_sqlalchemy_format(categories, brands_dict)
        res = {"total_pages": max(math.ceil(self.collection.estimated_document_count()/config.per_page), 1),
                "data" : categories}
        return res

    def create_sqlalchemy_format(self, categories, brands_dict):
        for category in categories:
            category["id"] = str(category["_id"])
            del category["_id"]
            this_brand = brands_dict.get(ObjectId(category["brand_id"]))
            category["brand_name"] = this_brand["name"]
            category["brand_id"] = this_brand["id"]
        return json.loads(json.dumps(categories))

    def query_brands(self):
        cursors = self.brand_col.find({})
        return list(cursors)

    def get_brands(self):
        cursors = self.brand_col.find({})
        return [{"id" : str(cursor["_id"]), "name" : cursor["name"]} for cursor in cursors]