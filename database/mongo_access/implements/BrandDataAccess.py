from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class BrandDataAccess(BaseDataAccess):
    def __init__(self, db, brand_model):
        super(BrandDataAccess, self).__init__(db, brand_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        brands = self.collection.find({}).skip(page*config.per_page - config.per_page).limit(config.per_page)
        res = {"total_pages": max(math.ceil(self.collection.estimated_document_count()/config.per_page), 1),
                "data" : [{"id" : str(city["_id"]), "name" : city["name"]} for city in brands]}
        return res