from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class StoreDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, address_col, district_col, city_col):
        super(StoreDataAccess, self).__init__(db, col_name)
        self.district_col = self.db.select(district_col)
        self.city_col = self.db.select(city_col)
        self.address_col = self.db.select(address_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        stores = self.collection.paginate(page, config.per_page)
        stores = self.create_sqlalchemy_format(stores, self.address_col.dict, self.district_col.dict, self.city_col.dict)
        res = {"total_pages": self.collection.get_pages(config.per_page),
                "data" : stores}
        return res

    def create_sqlalchemy_format(self, stores, addresses_dict, districts_dict, cities_dict):
        for store in stores:
            this_address = addresses_dict.get(ObjectId(store["address_id"]))
            store["address"] = this_address
            this_district = districts_dict.get(ObjectId(this_address["district_id"]))
            this_address["district"] = this_district
            this_district["city"] = cities_dict.get(ObjectId(this_district["city_id"]))
        return json.loads(json.dumps(stores))

    def get_cities(self):
        return self.city_col.list

    def get_districts(self):
        return self.district_col.list

    def get_addresses(self):
        for address in self.address_col.list:
            this_district = self.district_col.dict.get(ObjectId(address["district_id"]))
            address["district"] = this_district
            this_district["city"] = self.city_col.dict.get(ObjectId(this_district["city_id"]))
        return json.loads(json.dumps(self.address_col.list))

    def get_districts_by_city(self, **kwargs):
        districts = self.district_col.collection.find(kwargs)
        return [{"id" : str(district["_id"]), "name" : district["name"]} for district in districts]
