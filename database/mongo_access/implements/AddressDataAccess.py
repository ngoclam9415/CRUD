from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class AddressDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, district_col, city_col):
        super(AddressDataAccess, self).__init__(db, col_name)
        self.district_col = self.db.select(district_col)
        self.city_col = self.db.select(city_col)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        addresses = self.collection.paginate(page, config.per_page)
        addresses = self.create_sqlalchemy_format(addresses, self.district_col.dict, self.city_col.dict)
        print("addresses : ",addresses)
        res = {"total_page": self.collection.get_pages(config.per_page),
                "addresses" : addresses}
        return res

    def create_sqlalchemy_format(self, addresses, districts_dict, cities_dict):
        for address in addresses:
            this_district = districts_dict.get(ObjectId(address["district_id"]))
            address["district_id"] = this_district["id"]
            address["district"] = this_district["name"]
            address["city_id"] = cities_dict.get(ObjectId(this_district["city_id"]))["id"]
            address["city"] = cities_dict.get(ObjectId(this_district["city_id"]))["name"]
        return json.loads(json.dumps(addresses))

    def get_cities(self):
        return self.city_col.list

    def get_districts(self):
        return self.district_col.list

    def get_districts_by_city(self, **kwargs):
        datas = self.district_col.collection.find(kwargs)
        datas = list(datas)
        for data in datas:
            data["id"] = str(data["_id"])
            del data["_id"]
        return datas