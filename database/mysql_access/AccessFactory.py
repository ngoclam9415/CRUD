from database.mysql_access.implements.CityDataAccess import CityDataAccess
from database.mysql_access.implements.DistrictDataAccess import DistrictDataAccess
from database.mysql_access.models import db, City, District

class AccessFactory:
    def __init__(self):
        self.db = db
        self.city_access = CityDataAccess(self.db, City)
        self.district_access = DistrictDataAccess(self.db, District, City)

    def get_access(self, access_type):
        if access_type == "city":
            return self.city_access
        if access_type == "district":
            return self.district_access

    def init_app(self, app):
        self.db.init_app(app)