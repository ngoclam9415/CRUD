from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class ProductVariantDataAccess(BaseDataAccess):
    def __init__(self, db, product_variant_model, product_model, store_model, color_model):
        super(ProductVariantDataAccess, self).__init__(db, product_variant_model)
        self.product_model = product_model
        self.store_model = store_model
        self.color_model = color_model

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        product_variants = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)

        res = {
            "total_pages": product_variants.pages,
            "data": product_variants.items,
        }
        return res

    def get_products(self):
        return self.product_model.query.order_by(self.product_model.id).all()

    def get_colors(self):
        return self.color_model.query.order_by(self.color_model.value).all()

    def get_stores(self):
        return self.store_model.query.order_by(self.store_model.id).all()