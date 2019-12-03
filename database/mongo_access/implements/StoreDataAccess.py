from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class StoreDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, address_model, district_model, city_model):
        super(StoreDataAccess, self).__init__(db, col_name)
        self.district_model = self.db.select(district_model)
        self.city_model = self.db.select(city_model)
        self.address_model = self.db.select(address_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        stores = self.model.paginate(page, config.per_page)
        stores = self.create_sqlalchemy_format(stores)
        res = {"total_pages": self.model.get_pages(config.per_page),
                "data" : stores}
        return res

    def create_sqlalchemy_format(self, stores):
        for store in stores:
            this_address = self.get_this_address(store)
            store["address"] = this_address
            this_district = self.get_this_district(this_address)
            this_address["district"] = this_district
            this_district["city"] = self.get_this_city(this_district)
        return json.loads(json.dumps(stores))

    def get_cities(self):
        return self.city_model.list

    def get_districts(self):
        return self.district_model.list

    def get_addresses(self):
        for address in self.address_model.list:
            this_district = self.get_this_district(address)
            address["district"] = this_district
            this_district["city"] = self.get_this_city(this_district)
        return json.loads(json.dumps(self.address_model.list))

    def get_districts_by_city(self, **kwargs):
        districts = self.district_model.collection.find(kwargs)
        return [{"id" : str(district["_id"]), "name" : district["name"]} for district in districts]

    def create_item(self, **kwargs):
        result = super(StoreDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(StoreDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        this_address = self.get_this_address(result)
        this_district = self.get_this_district(this_address)
        this_city = self.get_this_city(this_district)
        return {"store_name" : result["store_name"], "address_detail" : this_address["detail"], 
                "district_name" : this_district["name"], "city_name" : this_city["name"], 
                "id" : str(result["_id"]), "type" : "store"}

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
            print("mongo_district_id : ",mongo_district_id)
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