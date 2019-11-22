from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class AddressDataAccess(BaseDataAccess):
    def __init__(self, db, address_model, district_model, city_model):
        super(AddressDataAccess, self).__init__(db, address_model)
        self.district_model = district_model
        self.city_model = city_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        addresses = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        arr_address = [{'city': address.district.city.name, 'city_id': address.district.city.id,
                        'district': address.district.name, 'district_id': address.district.id,
                        'detail': address.detail, 'id': address.id}
                        for address in addresses.items]
        res = {"addresses" : arr_address, "total_page" : addresses.pages}
                    
        return res

    def get_cities(self):
        return [city for city in self.city_model.query.all()]

    def get_districts_by_city(self, **kwargs):
        districts = self.district_model.query.filter_by(**kwargs).all()
        return [{'id': district.id, 'name': district.name}
                         for district in districts]