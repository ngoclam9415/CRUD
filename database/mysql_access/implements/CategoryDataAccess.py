from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class CategoryDataAccess(BaseDataAccess):
    def __init__(self, db, category_model, brand_model):
        super(CategoryDataAccess, self).__init__(db, category_model)
        self.brand_model = brand_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        categories = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        arr_category = []
        for category in categories.items:
            tmp_category = {
                'id': category.id,
                'name': category.name,
                'brand_name': category.brand.name,
                'brand_id' : category.brand.id
            }
            arr_category.append(tmp_category)
        
        res = {
            "total_pages": categories.pages,
            "data": arr_category,
        }
        return res

    def get_brands(self):
        brands = self.brand_model.query.all()
        brands = [{"id" : brand.id, "name" : brand.name} for brand in brands]
        return brands