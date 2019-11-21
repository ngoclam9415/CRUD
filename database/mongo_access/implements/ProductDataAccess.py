from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json

class ProductDataAccess(BaseDataAccess):
    def __init__(self, db, product_col, category_col, brand_col):
        super(ProductDataAccess, self).__init__(db, product_col)
        self.category_col = db.select(category_col)
        self.brand_col = db.select(brand_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        products = self.collection.paginate(page, config.per_page)
        products = self.create_sqlalchemy_format(products, self.category_col.dict, self.brand_col.dict)
        res = {"total_pages" : self.collection.get_pages(config.per_page),
                "data" : products}
        return res

    def create_sqlalchemy_format(self, products, categories_dict, brands_dict):
        for product in products:
            this_category = categories_dict.get(ObjectId(product["category_id"]))
            this_category["brand"] = brands_dict.get(ObjectId(this_category["brand_id"]))
            product["category"] = this_category
        return json.loads(json.dumps(products))

    def get_categories(self):
        for category in self.category_col.list:
            category["brand"] = self.brand_col.dict.get(ObjectId(category["brand_id"]))
        return json.loads(json.dumps(self.category_col.list))
    

    