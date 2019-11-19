from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class StoreDataAccess(BaseDataAccess):
    def __init__(self, db, store_model, address_model):
        super(StoreDataAccess, self).__init__(db, store_model)
        self.address_model = address_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        stores = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        res = {
            "total_pages": stores.pages,
            "data": stores.items,
        }
        return res

    def get_addresses(self):
        return self.address_model.query.order_by(self.address_model.id).all()