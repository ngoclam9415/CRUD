from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class CityDataAccess(BaseDataAccess):
    def __init__(self, db, city_model):
        super(CityDataAccess, self).__init__(db, city_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        cities = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        arr_city = []
        for city in cities.items:
            tmp_city = {
                'id': city.id,
                'name': city.name
            }
            arr_city.append(tmp_city)
        res = {
            "total_pages": cities.pages,
            "data": arr_city,
        }
        return res