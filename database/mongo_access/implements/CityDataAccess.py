from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class CityDataAccess(BaseDataAccess):
    def __init__(self, db, col_name):
        super(CityDataAccess, self).__init__(db, col_name)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        res = {"total_pages": max(math.ceil(self.collection.estimated_document_count()/config.per_page), 1),
                "data" : [{"id" : str(city["_id"]), "name" : city["name"]} for city in cities]}
        return res

