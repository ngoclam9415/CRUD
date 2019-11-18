from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class BrandDataAccess(BaseDataAccess):
    def __init__(self, db, brand_model):
        super(BrandDataAccess, self).__init__(db, brand_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        brands = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        arr_brand = []
        for brand in brands.items:
            tmp_brand = {
                'id': brand.id,
                'name': brand.name
            }
            arr_brand.append(tmp_brand)
        res = {
            "total_pages": brands.pages,
            "data": arr_brand,
        }
        return res