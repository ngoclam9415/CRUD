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
        variants = self.create_sqlalchemy_format(variants, self.product_col.dict, self.category_col.dict, self.brand_col.dict, self.store_col.dict, self.address_col.dict, self.district_col.dict, self.city_col.dict, self.color_col.dict)
        res = {"total_pages" : self.collection.get_pages(config.per_page),
            "data" : variants}
        return res
        

    def create_sqlalchemy_format(self, variants, product_dict, category_dict, brand_dict, store_dict, address_dict, district_dict, city_dict, color_dict):
        for variant in variants:
            this_product = product_dict.get(ObjectId(variant["product_id"]))
            this_category = category_dict.get(ObjectId(this_product["category_id"]))
            this_brand = brand_dict.get(ObjectId(this_category["brand_id"]))
            this_store = store_dict.get(ObjectId(variant["store_id"]))
            this_address = address_dict.get(ObjectId(this_store["address_id"]))
            this_district = district_dict.get(ObjectId(this_address["district_id"]))
            this_city = city_dict.get(ObjectId(this_district["city_id"]))
            this_color = color_dict.get(ObjectId(variant["color_id"]))
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
            this_category = self.category_col.dict.get(ObjectId(product["category_id"]))
            this_category["brand"] = self.brand_col.dict.get(ObjectId(this_category["brand_id"]))
            product["category"] = this_category
        return json.loads(json.dumps(self.product_col.list))


    def get_stores(self):
        for store in self.store_col.list:
            this_address = self.address_col.dict.get(ObjectId(store["address_id"]))
            this_district = self.district_col.dict.get(ObjectId(this_address["district_id"]))
            this_city = self.city_col.dict.get(ObjectId(this_district["city_id"]))
            this_address["district"] = this_district
            this_district["city"] = this_city
            store["address"] = this_address
        return json.loads(json.dumps(self.store_col.list))

    def get_colors(self):
        return json.loads(json.dumps(self.color_col.list))