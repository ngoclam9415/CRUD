from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class BrandDataAccess(BaseDataAccess):
    def __init__(self, db, brand_model):
        super(BrandDataAccess, self).__init__(db, brand_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        brands = self.collection.paginate(page, config.per_page)
        res = {"total_pages": self.collection.get_pages(config.per_page),
                "data" : brands}
        return res