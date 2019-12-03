from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json

class ProductVariantDataAccess(BaseDataAccess):
    def __init__(self, db, variant_col, product_model, category_model, brand_model, store_model, address_model, district_model, city_model, color_model):
        super(ProductVariantDataAccess, self).__init__(db, variant_col)
        self.product_model = db.select(product_model)
        self.category_model = db.select(category_model)  
        self.brand_model = db.select(brand_model)
        self.store_model = db.select(store_model)
        self.address_model = db.select(address_model)
        self.district_model = db.select(district_model)
        self.city_model = db.select(city_model)
        self.color_model = db.select(color_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        variants = self.model.paginate(page, config.per_page)
        variants = self.create_sqlalchemy_format(variants)
        res = {"total_pages" : self.model.get_pages(config.per_page),
            "data" : variants}
        return res
        

    def create_sqlalchemy_format(self, variants):
        for variant in variants:
            this_product = self.get_this_product(variant)
            this_category = self.get_this_category(this_product)
            this_brand = self.get_this_brand(this_category)
            this_store = self.get_this_store(variant)
            this_address = self.get_this_address(this_store)
            this_district = self.get_this_district(this_address)
            this_city = self.get_this_city(this_district)
            this_color = self.get_this_color(variant)
            this_product["category"] = this_category
            this_category["brand"] = this_brand
            this_store["address"] = this_address
            this_address["district"] = this_district
            this_district["city"] = this_city
            variant["product"] = this_product
            variant["store"] = this_store
            variant["color"] = this_color
        return json.loads(json.dumps(variants))

    def get_products(self):
        for product in self.product_model.list:
            this_category = self.get_this_category(product)
            this_category["brand"] = self.get_this_brand(this_category)
            product["category"] = this_category
        return json.loads(json.dumps(self.product_model.list))


    def get_stores(self):
        for store in self.store_model.list:
            this_address = self.get_this_address(store)
            this_district = self.get_this_district(this_address)
            this_city = self.get_this_city(this_district)
            this_address["district"] = this_district
            this_district["city"] = this_city
            store["address"] = this_address
        return json.loads(json.dumps(self.store_model.list))

    def get_colors(self):
        return json.loads(json.dumps(self.color_model.list))

    def create_item(self, **kwargs):
        result = super(ProductVariantDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(ProductVariantDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        this_product = self.get_this_product(result)
        this_category = self.get_this_category(this_product)
        this_brand = self.get_this_brand(this_category)
        this_store = self.get_this_store(result)
        this_address = self.get_this_address(this_store)
        this_district = self.get_this_district(this_address)
        this_city = self.get_this_city(this_district)
        this_color = self.get_this_color(result)
        return {"variant_price" : result["price"], "product_name" : this_product["name"], 
                "category_name" : this_category["name"], "brand_name" : this_brand["name"],
                "store_name" : this_store["store_name"], "address_detail" : this_address["detail"],
                "city_name" : this_city["name"], "color_value" : this_color["value"], "district_name" : this_district["name"],
                "id" : str(result["_id"]), "type" : "variant"}


    def get_this_city(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.city_model.collection.name,
                                        "mysql_id" : int(result["city_id"])})
            mongo_city_id = cursor["mongo_id"]
            this_city = self.model.redis_accessor.load(mongo_city_id)
        else:
            this_city = self.model.redis_accessor.load(result["city_id"])
        return this_city

    def get_this_district(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.district_model.collection.name,
                                        "mysql_id" : int(result["district_id"])})
            mongo_district_id = cursor["mongo_id"]
            this_district = self.model.redis_accessor.load(mongo_district_id)
        else:
            this_district = self.model.redis_accessor.load(result["district_id"])
        return this_district

    def get_this_address(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.address_model.collection.name,
                                        "mysql_id" : int(result["address_id"])})
            mongo_address_id = cursor["mongo_id"]
            this_address = self.model.redis_accessor.load(mongo_address_id)
        else:
            this_address = self.model.redis_accessor.load(result["address_id"])
        return this_address

    def get_this_store(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.store_model.collection.name,
                                        "mysql_id" : int(result["store_id"])})
            mongo_store_id = cursor["mongo_id"]
            this_store = self.model.redis_accessor.load(mongo_store_id)
        else:
            this_store = self.model.redis_accessor.load(result["store_id"])
        return this_store

    def get_this_brand(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.brand_model.collection.name,
                                        "mysql_id" : int(result["brand_id"])})
            mongo_brand_id = cursor["mongo_id"]
            this_brand = self.model.redis_accessor.load(mongo_brand_id)
        else:
            this_brand = self.model.redis_accessor.load(result["brand_id"])
        return this_brand

    def get_this_category(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.category_model.collection.name,
                                        "mysql_id" : int(result["category_id"])})
            mongo_category_id = cursor["mongo_id"]
            this_category = self.model.redis_accessor.load(mongo_category_id)
        else:
            this_category = self.model.redis_accessor.load(result["category_id"])
        return this_category

    def get_this_product(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.product_model.collection.name,
                                        "mysql_id" : int(result["product_id"])})
            mongo_product_id = cursor["mongo_id"]
            this_product = self.model.redis_accessor.load(mongo_product_id)
        else:
            this_product = self.model.redis_accessor.load(result["product_id"])
        return this_product

    def get_this_color(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.color_model.collection.name,
                                        "mysql_id" : int(result["color_id"])})
            mongo_color_id = cursor["mongo_id"]
            this_color = self.model.redis_accessor.load(mongo_color_id)
        else:
            this_color = self.model.redis_accessor.load(result["color_id"])
        return this_color
