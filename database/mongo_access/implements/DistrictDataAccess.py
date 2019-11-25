from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import math
import json

class DistrictDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, city_col_name):
        super(DistrictDataAccess, self).__init__(db, col_name)
        self.city_col = db.select(city_col_name)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        districts = self.collection.paginate(page, config.per_page)
        districts = self.create_sqlalchemy_format(districts)
        res = {"pages": self.collection.get_pages(config.per_page),
                "cities" : self.city_col.list, 
                "infos" : districts}
        return res

    def create_sqlalchemy_format(self, districts):
        for district in districts:
            district["city"] = self.collection.redis_accessor.load(district["city_id"])
        return json.loads(json.dumps(districts))

    def get_cities(self):
        return self.city_col.list

    def create_item(self, **kwargs):
        result = super(DistrictDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.collection.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(DistrictDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.collection.edit_search_item(**data)

    def create_search_data(self, result):
        this_city = self.collection.redis_accessor.load(result["city_id"])
        return {"district_name" : result["name"], "city_name" : this_city["name"], "id" : str(result["_id"]), "type" : "district"}
