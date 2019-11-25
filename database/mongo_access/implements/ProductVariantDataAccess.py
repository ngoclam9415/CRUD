from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json

class ProductVariantDataAccess(BaseDataAccess):
    def __init__(self, db, variant_col, product_col, category_col, brand_col, store_col, address_col, district_col, city_col, color_col):
        super(ProductVariantDataAccess, self).__init__(db, variant_col)
        self.product_col = db.select(product_col)
        self.category_col = db.select(category_col)  
        self.brand_col = db.select(brand_col)
        self.store_col = db.select(store_col)
        self.address_col = db.select(address_col)
        self.district_col = db.select(district_col)
        self.city_col = db.select(city_col)
        self.color_col = db.select(color_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        variants = self.collection.paginate(page, config.per_page)
        variants = self.create_sqlalchemy_format(variants)
        res = {"total_pages" : self.collection.get_pages(config.per_page),
            "data" : variants}
        return res
        

    def create_sqlalchemy_format(self, variants):
        for variant in variants:
            this_product = self.collection.redis_accessor.load(variant["product_id"])
            this_category = self.collection.redis_accessor.load(this_product["category_id"])
            this_brand = self.collection.redis_accessor.load(this_category["brand_id"])
            this_store = self.collection.redis_accessor.load(variant["store_id"])
            this_address = self.collection.redis_accessor.load(this_store["address_id"])
            this_district = self.collection.redis_accessor.load(this_address["district_id"])
            this_city = self.collection.redis_accessor.load(this_district["city_id"])
            this_color = self.collection.redis_accessor.load(variant["color_id"])
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
        for product in self.product_col.list:
            this_category = self.collection.redis_accessor.load(product["category_id"])
            this_category["brand"] = self.collection.redis_accessor.load(this_category["brand_id"])
            product["category"] = this_category
        return json.loads(json.dumps(self.product_col.list))


    def get_stores(self):
        for store in self.store_col.list:
            this_address = self.collection.redis_accessor.load(store["address_id"])
            this_district = self.collection.redis_accessor.load(this_address["district_id"])
            this_city = self.collection.redis_accessor.load(this_district["city_id"])
            this_address["district"] = this_district
            this_district["city"] = this_city
            store["address"] = this_address
        return json.loads(json.dumps(self.store_col.list))

    def get_colors(self):
        return json.loads(json.dumps(self.color_col.list))

    def create_item(self, **kwargs):
        result = super(ProductVariantDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.collection.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(ProductVariantDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.collection.edit_search_item(**data)

    def create_search_data(self, result):
        this_product = self.collection.redis_accessor.load(result["product_id"])
        this_category = self.collection.redis_accessor.load(this_product["category_id"])
        this_brand = self.collection.redis_accessor.load(this_category["brand_id"])
        this_store = self.collection.redis_accessor.load(result["store_id"])
        this_address = self.collection.redis_accessor.load(this_store["address_id"])
        this_district = self.collection.redis_accessor.load(this_address["district_id"])
        this_city = self.collection.redis_accessor.load(this_district["city_id"])
        this_color = self.collection.redis_accessor.load(result["color_id"])
        return {"variant_price" : result["price"], "product_name" : this_product["name"], 
                "category_name" : this_category["name"], "brand_name" : this_brand["name"],
                "store_name" : this_store["store_name"], "address_detail" : this_address["detail"],
                "city_name" : this_city["name"], "color_value" : this_color["value"], "district_name" : this_district["name"],
                "id" : str(result["_id"]), "type" : "variant"}
