from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class ProductDataAccess(BaseDataAccess):
    def __init__(self, db, product_model, category_model):
        super(ProductDataAccess, self).__init__(db, product_model)
        self.category_model = category_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        products = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        res = {
            "total_pages": products.pages,
            "data": [{'id' : product.id, 'name' : product.name, 'category_name' : product.category.name} for product in products.items]
        }
        return res

    def get_categories(self):
        return self.category_model.query.order_by(self.category_model.id).all()