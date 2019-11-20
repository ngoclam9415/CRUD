from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class AddressDataAccess(BaseDataAccess):
    def __init__(self, db, col_name):
        super(AddressDataAccess, self).__init__(db, col_name)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        addresses = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        res = {"total_page": math.ceil(self.collection.estimated_data_count()/config.per_page),
                "data" : 

