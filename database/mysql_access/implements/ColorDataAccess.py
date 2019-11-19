from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config

class ColorDataAccess(BaseDataAccess):
    def __init__(self, db, color_model):
        super(ColorDataAccess, self).__init__(db, color_model)

    def list_item(self, **kwargs):
        page = kwargs.get("page", 1)
        colors = self.model.query.order_by(self.model.id).paginate(page, config.per_page, error_out=False)
        res = {
            "total_pages": colors.pages,
            "data": colors.items,
        }

        return res