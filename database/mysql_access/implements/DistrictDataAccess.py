from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class DistrictDataAccess(BaseDataAccess):
    def __init__(self, db, district_model, city_model):
        super(DistrictDataAccess, self).__init__(db, district_model)
        self.city_model = city_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.city_model.query.all()
        results = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        res = {"cities" : cities, "pages" : results.pages, "infos": results.items}
        return res