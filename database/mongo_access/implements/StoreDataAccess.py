from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class StoreDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, address_col, district_col, city_col):
        super(StoreDataAccess, self).__init__(db, col_name)
        self.district_col = self.db.add_collection(district_col)
        self.city_col = self.db.add_collection(city_col)
        self.address_col = self.db.add_collection(address_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.query_cities()
        districts = self.query_districts()
        addresses = self.query_addresses()
        stores = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        cities_dict, cities_list = self.parse(cities)
        districts_dict, districts_list = self.parse(districts)
        addresses_dict, addresses_list = self.parse(addresses)
        stores = list(stores)
        stores = self.create_sqlalchemy_format(stores, addresses_dict, districts_dict, cities_dict)
        res = {"total_pages": max(math.ceil(self.collection.estimated_document_count()/config.per_page), 1),
                "data" : stores}
        return res

    def create_sqlalchemy_format(self, stores, addresses_dict, districts_dict, cities_dict):
        for store in stores:
            store["id"] = str(store["_id"])
            del store["_id"]
            this_address = addresses_dict.get(ObjectId(store["address_id"]))
            store["address"] = this_address
            this_district = districts_dict.get(ObjectId(this_address["district_id"]))
            this_address["district"] = this_district
            this_district["city"] = cities_dict.get(ObjectId(this_district["city_id"]))
        return json.loads(json.dumps(stores))

    def query_cities(self):
        cities = self.city_col.find({})
        cities = list(cities)
        return list(cities)

    def query_districts(self):
        districts = self.district_col.find({})
        districts = list(districts)
        return list(districts)

    def query_addresses(self):
        addresses = self.address_col.find({})
        addresses = list(addresses)
        return list(addresses)

    def get_cities(self):
        cities = self.query_cities()
        for city in cities:
            city["id"] = str(city["_id"])
        return cities

    def get_districts(self):
        districts = self.query_districts()
        for district in districts:
            district["id"] = str(district["_id"])
        return districts

    def get_addresses(self):
        cities = self.query_cities()
        districts = self.query_districts()
        addresses = self.query_addresses()
        cities_dict, cities_list = self.parse(cities)
        districts_dict, districts_list = self.parse(districts)
        addresses_dict, addresses_list = self.parse(addresses)
        for address in addresses_list:
            this_district = districts_dict.get(ObjectId(address["district_id"]))
            address["district"] = this_district
            this_district["city"] = cities_dict.get(ObjectId(this_district["city_id"]))
        return json.loads(json.dumps(addresses_list))

    def get_districts_by_city(self, **kwargs):
        districts = self.district_col.find(kwargs)
        return [{"id" : str(district["_id"]), "name" : district["name"]} for district in districts]
