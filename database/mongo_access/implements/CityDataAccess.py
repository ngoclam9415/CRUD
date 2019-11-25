from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class CityDataAccess(BaseDataAccess):
    def __init__(self, db, col_name):
        super(CityDataAccess, self).__init__(db, col_name)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.collection.paginate(page, config.per_page)
        res = {"total_pages": self.collection.get_pages(config.per_page),
                "data" : cities}
        return res

    def create_item(self, **kwargs):
        result = super(CityDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.collection.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(CityDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.collection.edit_search_item(**data)

    def create_search_data(self, result):
        return {"city_name" : result["name"], "id" : str(result["_id"]), "type" : "city"}
