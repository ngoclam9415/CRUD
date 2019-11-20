from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class AddressDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, district_col, city_col):
        super(AddressDataAccess, self).__init__(db, col_name)
        self.district_col = self.db.add_collection(district_col)
        self.city_col = self.db.add_collection(city_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.query_cities()
        districts = self.query_districts()
        addresses = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        cities_dict, cities_list = self.parse(cities)
        districts_dict, districts_list = self.parse(districts)
        addresses = list(addresses) 
        addresses = self.create_sqlalchemy_format(addresses, districts_dict, cities_dict)
        print("addresses : ",addresses)
        res = {"total_page": max(math.ceil(self.collection.estimated_document_count()/config.per_page), 1),
                "addresses" : addresses}
        return res

    def create_sqlalchemy_format(self, addresses, districts_dict, cities_dict):

        for address in addresses:
            address["id"] = str(address["_id"])
            del address["_id"]
            this_district = districts_dict.get(ObjectId(address["district_id"]))
            address["district_id"] = this_district["id"]
            address["district"] = this_district["name"]
            address["city_id"] = cities_dict.get(ObjectId(this_district["city_id"]))["id"]
            address["city"] = cities_dict.get(ObjectId(this_district["city_id"]))["name"]
        return json.loads(json.dumps(addresses))

    def query_cities(self):
        cities = self.city_col.find({})
        cities = list(cities)
        return list(cities)

    def query_districts(self):
        districts = self.district_col.find({})
        districts = list(districts)
        return list(districts)

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

    def get_districts_by_city(self, **kwargs):
        districts = self.district_col.find(kwargs)
        return [{"id" : str(district["_id"]), "name" : district["name"]} for district in districts]
