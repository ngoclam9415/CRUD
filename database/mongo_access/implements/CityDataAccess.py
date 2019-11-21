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

