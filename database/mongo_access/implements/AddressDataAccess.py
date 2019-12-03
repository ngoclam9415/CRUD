from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from bson.objectid import ObjectId
import math
import json

class AddressDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, district_model, city_model):
        super(AddressDataAccess, self).__init__(db, col_name)
        self.district_model = self.db.select(district_model)
        self.city_model = self.db.select(city_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        addresses = self.model.paginate(page, config.per_page)
        addresses = self.create_sqlalchemy_format(addresses)
        res = {"total_page": self.model.get_pages(config.per_page),
                "addresses" : addresses}
        return res

    def create_item(self, **kwargs):
        result = super(AddressDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(AddressDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        this_district = self.get_this_district(result)
        this_city = self.get_this_city(this_district)
        return {"address_detail" : result["detail"], "district_name" : this_district["name"], "city_name" : this_city["name"], "id" : str(result["_id"]), "type" : "address"}

    def create_sqlalchemy_format(self, addresses):
        for address in addresses:
            this_district = self.get_this_district(address)
            address["district_id"] = this_district["id"]
            address["district"] = this_district["name"]
            this_city = self.get_this_city(this_district)
            address["city_id"] = this_city["id"]
            address["city"] = this_city["name"]
        return json.loads(json.dumps(addresses))

    def get_this_district(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.district_model.collection.name,
                                        "mysql_id" : int(result["district_id"])})
            mongo_district_id = cursor["mongo_id"]
            this_district = self.model.redis_accessor.load(mongo_district_id)
        else:
            this_district = self.model.redis_accessor.load(result["district_id"])
        return this_district

    def get_this_city(self, result):
        if "mysql_id" in result.keys():
            cursor = self.model.sync_col.find_one({"col_type" : self.city_model.collection.name,
                                        "mysql_id" : int(result["city_id"])})
            mongo_city_id = cursor["mongo_id"]
            this_city = self.model.redis_accessor.load(mongo_city_id)
        else:
            this_city = self.model.redis_accessor.load(result["city_id"])
        return this_city

    def get_cities(self):
        return self.city_model.list

    def get_districts(self):
        return self.district_model.list

    def get_districts_by_city(self, **kwargs):
        datas = self.district_model.collection.find(kwargs)
        datas = list(datas)
        for data in datas:
            data["id"] = str(data["_id"])
            del data["_id"]
        return datas