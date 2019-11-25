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
        products = self.create_sqlalchemy_format(products)
        res = {"total_pages" : self.collection.get_pages(config.per_page),
                "data" : products}
        return res

    def create_sqlalchemy_format(self, products):
        for product in products:
            this_category = self.collection.redis_accessor.load(product["category_id"])
            this_category["brand"] = self.collection.redis_accessor.load(this_category["brand_id"])
            product["category"] = this_category
        return json.loads(json.dumps(products))

    def get_categories(self):
        for category in self.category_col.list:
            category["brand"] = self.collection.redis_accessor.load(category["brand_id"])
        return json.loads(json.dumps(self.category_col.list))
    
    def create_item(self, **kwargs):
        result = super(ProductDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.collection.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(ProductDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.collection.edit_search_item(**data)

    def create_search_data(self, result):
        this_category = self.collection.redis_accessor.load(result["category_id"])
        this_brand = self.collection.redis_accessor.load(this_category["brand_id"])
        return {"product_name" : result["name"], "category_name" : this_category["name"], "brand_name" : this_brand["name"], "id" : str(result["_id"]), "type" : "product"}