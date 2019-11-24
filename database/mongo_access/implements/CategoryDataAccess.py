from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json
import math

class CategoryDataAccess(BaseDataAccess):
    def __init__(self, db, category_model, brand_col):
        super(CategoryDataAccess, self).__init__(db, category_model)
        self.brand_col = db.select(brand_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        categories = self.collection.paginate(page, config.per_page)
        categories = self.create_sqlalchemy_format(categories)
        res = {"total_pages": self.collection.get_pages(config.per_page),
                "data" : categories}
        return res

    def create_sqlalchemy_format(self, categories):
        for category in categories:
            this_brand = self.collection.redis_accessor.load(category["brand_id"])
            category["brand_name"] = this_brand["name"]
            category["brand_id"] = this_brand["id"]
        return json.loads(json.dumps(categories))

    def get_brands(self):
        return self.brand_col.list