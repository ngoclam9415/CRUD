from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math

class SearchDataAccess(BaseDataAccess):
    def __init__(self, db, search_model):
        super(SearchDataAccess, self).__init__(db, search_model)

    def show_searched_item(self, text):
        return self.model.show_searched_item(text)

    def create_item(self, **kwargs):
        result = super(SearchDataAccess, self).create_item(**kwargs)
        data = self.create_search_data(result)
        self.model.create_search_item(**data)

    def edit_item(self, id, **kwargs):
        result = super(SearchDataAccess, self).edit_item(id, **kwargs)
        data = self.create_search_data(result)
        self.model.edit_search_item(**data)

    def create_search_data(self, result):
        return {"search_name" : result["name"], "id" : str(result["_id"]), "type" : "search"}

if __name__ == "__main__":
    from database.mongo_access.models import db
    sdb = SearchDataAccess(db, "Search")
    sdb.show_searched_item("University")