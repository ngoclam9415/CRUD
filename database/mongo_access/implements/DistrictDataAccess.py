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
        districts = self.create_sqlalchemy_format(districts, self.city_col.dict)
        res = {"pages": self.collection.get_pages(config.per_page),
                "cities" : self.city_col.list, 
                "infos" : districts}
        return res

    def create_sqlalchemy_format(self, districts, cities_dict):
        for district in districts:
            district["city"] = cities_dict.get(ObjectId(district["city_id"]))
        return json.loads(json.dumps(districts))

    def get_cities(self):
        return self.city_col.list
