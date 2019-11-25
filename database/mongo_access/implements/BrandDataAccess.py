from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class BrandDataAccess(BaseDataAccess):
    def __init__(self, db, brand_model):
        super(BrandDataAccess, self).__init__(db, brand_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        brands = self.model.paginate(page, config.per_page)
        res = {"total_pages": self.model.get_pages(config.per_page),
                "data" : brands}
        return res

    def create_item(self, **kwargs):
        result = super(BrandDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(BrandDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        return {"brand_name" : result["name"], "id" : str(result["_id"]), "type" : "brand"}