from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import math
import json

class DistrictDataAccess(BaseDataAccess):
    def __init__(self, db, col_name, city_col_name):
        super(DistrictDataAccess, self).__init__(db, col_name)
        self.city_col = db.add_collection(city_col_name)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.query_cities()
        districts = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        cities_dict, cities_list = self.parse(cities)
        districts = list(districts) 
        districts = self.create_sqlalchemy_format(districts, cities_dict)
        print("districts : ",districts)
        res = {"pages": math.ceil(self.collection.estimated_document_count()/config.per_page),
                "cities" : cities_list, 
                "infos" : districts}
        return res

    def create_sqlalchemy_format(self, districts, cities_dict):
        for district in districts:
            district["id"] = str(district["_id"])
            del district["_id"]
            district["city"] = cities_dict.get(ObjectId(district["city_id"]))
        return json.loads(json.dumps(districts))

    def query_cities(self):
        cities = self.city_col.find({})
        cities = list(cities)
        return list(cities)

    def get_cities(self):
        cities = self.query_cities()
        for city in cities:
            city["id"] = str(city["_id"])
        return cities
