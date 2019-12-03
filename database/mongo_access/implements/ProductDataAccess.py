from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json

class ProductDataAccess(BaseDataAccess):
    def __init__(self, db, product_col, category_model, brand_model):
        super(ProductDataAccess, self).__init__(db, product_col)
        self.category_model = db.select(category_model)
        self.brand_model = db.select(brand_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        products = self.model.paginate(page, config.per_page)
        products = self.create_sqlalchemy_format(products)
        res = {"total_pages" : self.model.get_pages(config.per_page),
                "data" : products}
        return res

    def create_sqlalchemy_format(self, products):
        for product in products:
            this_category = self.get_this_category(product)
            this_category["brand"] = self.get_this_brand(this_category)
            product["category"] = this_category
        return json.loads(json.dumps(products))

    def get_categories(self):
        for category in self.category_model.list:
            category["brand"] = self.get_this_brand(category)
        return json.loads(json.dumps(self.category_model.list))
    
    def create_item(self, **kwargs):
        result = super(ProductDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(ProductDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        this_category = self.get_this_category(result)
        this_brand = self.get_this_brand(this_category)
        return {"product_name" : result["name"], "category_name" : this_category["name"], "brand_name" : this_brand["name"], "id" : str(result["_id"]), "type" : "product"}

    def get_this_category(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.category_model.collection.name,
                                        "mysql_id" : int(result["category_id"])})
            mongo_category_id = cursor["mongo_id"]
            this_category = self.model.redis_accessor.load(mongo_category_id)
        else:
            this_category = self.model.redis_accessor.load(result["category_id"])
        return this_category

    def get_this_brand(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.brand_model.collection.name,
                                        "mysql_id" : int(result["brand_id"])})
            mongo_brand_id = cursor["mongo_id"]
            this_brand = self.model.redis_accessor.load(mongo_brand_id)
        else:
            this_brand = self.model.redis_accessor.load(result["brand_id"])
        return this_brand