from database.mysql_access.implements.CityDataAccess import CityDataAccess
from database.mysql_access.implements.DistrictDataAccess import DistrictDataAccess
from database.mysql_access.implements.BrandDataAccess import BrandDataAccess
from database.mysql_access.implements.CategoryDataAccess import CategoryDataAccess
from database.mysql_access.implements.ColorDataAccess import ColorDataAccess
from database.mysql_access.implements.AddressDataAccess import AddressDataAccess
from database.mysql_access.implements.StoreDataAccess import StoreDataAccess
from database.mysql_access.implements.AddressDataAccess import AddressDataAccess
from database.mysql_access.implements.AddressDataAccess import AddressDataAccess
from database.mysql_access.models import db, City, District, Brand, Category, Address, Color, Store

class AccessFactory:
    def __init__(self):
        self.db = db
        self.city_access = CityDataAccess(self.db, City)
        self.district_access = DistrictDataAccess(self.db, District, City)
        self.brand_access = BrandDataAccess(self.db, Brand)
        self.category_access = CategoryDataAccess(self.db, Category, Brand)
        self.address_access = AddressDataAccess(self.db, Address, District, City)
        self.color_access = ColorDataAccess(self.db, Color)
        self.store_access = StoreDataAccess(self.db, Store, Address)

    def get_access(self, access_type):
        if access_type == "city":
            return self.city_access
        elif access_type == "district":
            return self.district_access
        elif access_type == "brand":
            return self.brand_access
        elif access_type == "category":
            return self.category_access
        elif access_type == "address":
            return self.address_access
        elif access_type == "color":
            return self.color_access
        elif access_type == "store":
            return self.store_access

    def init_app(self, app):
        self.db.init_app(app)