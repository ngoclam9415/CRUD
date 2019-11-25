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
        addresses = self.create_sqlalchemy_format(addresses)
        res = {"total_page": self.collection.get_pages(config.per_page),
                "addresses" : addresses}
        return res

    def create_item(self, **kwargs):
        result = super(AddressDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.collection.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(AddressDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.collection.edit_search_item(**data)

    def create_search_data(self, result):
        this_district = self.collection.redis_accessor.load(result["district_id"])
        this_city = self.collection.redis_accessor.load(this_district["city_id"])
        return {"address_detail" : result["detail"], "district_name" : this_district["name"], "city_name" : this_city["name"], "id" : str(result["_id"]), "type" : "address"}

    def create_sqlalchemy_format(self, addresses):
        for address in addresses:
            this_district = self.collection.redis_accessor.load(address["district_id"])
            address["district_id"] = this_district["id"]
            address["district"] = this_district["name"]
            address["city_id"] = self.collection.redis_accessor.load(this_district["city_id"])["id"]
            address["city"] = self.collection.redis_accessor.load(this_district["city_id"])["name"]
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