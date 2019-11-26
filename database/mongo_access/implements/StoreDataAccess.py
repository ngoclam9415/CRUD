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
            this_address = self.model.redis_accessor.load(store["address_id"])
            store["address"] = this_address
            this_district = self.model.redis_accessor.load(this_address["district_id"])
            this_address["district"] = this_district
            this_district["city"] = self.model.redis_accessor.load(this_district["city_id"])
        return json.loads(json.dumps(stores))

    def get_cities(self):
        return self.city_model.list

    def get_districts(self):
        return self.district_model.list

    def get_addresses(self):
        for address in self.address_model.list:
            this_district = self.model.redis_accessor.load(address["district_id"])
            address["district"] = this_district
            this_district["city"] = self.model.redis_accessor.load(this_district["city_id"])
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
        this_address = self.model.redis_accessor.load(result["address_id"])
        this_district = self.model.redis_accessor.load(this_address["district_id"])
        this_city = self.model.redis_accessor.load(this_district["city_id"])
        return {"store_name" : result["store_name"], "address_detail" : this_address["detail"], 
                "district_name" : this_district["name"], "city_name" : this_city["name"], 
                "id" : str(result["_id"]), "type" : "store"}
