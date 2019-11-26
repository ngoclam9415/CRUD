from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from sqlalchemy_fulltext import FullText, FullTextSearch
import sqlalchemy_fulltext.modes as FullTextMode
from sqlalchemy import Index, or_
from sqlalchemy.orm import sessionmaker

class SearchDataAccess(BaseDataAccess):
    def __init__(self, db, variant_col, product_model, category_model, brand_model, store_model, address_model, district_model, city_model, color_model):
        super(SearchDataAccess, self).__init__(db, variant_col)
        self.product_model = product_model
        self.category_model = category_model
        self.brand_model = brand_model
        self.store_model = store_model
        self.address_model = address_model
        self.district_model = district_model
        self.city_model = city_model
        self.color_model = color_model
        
 

    def show_searched_item(self, text):
        data = {}
        self.check_or_create_session()
        data = self.get_city_search_result(data, text)
        data = self.get_district_search_result(data, text)
        data = self.get_address_search_result(data, text)
        data = self.get_store_search_result(data, text)
        data = self.get_color_search_result(data, text)
        data = self.get_brand_search_result(data, text)
        data = self.get_category_search_result(data, text)
        data = self.get_product_search_result(data, text)
        data = self.get_variant_search_result(data, text)
        return data

    def get_city_search_result(self,result, text):
        cities = self.session.query(self.city_model).filter(FullTextSearch(text, self.city_model, FullTextMode.BOOLEAN)).all()
        result["city"] = [{"city_name" : city.name, "_id" : city.id} for city in cities]
        return result

    def get_district_search_result(self, result, text):
        districts = self.session.query(self.district_model).join(self.city_model, self.district_model.city_id == self.city_model.id).filter(or_(FullTextSearch(text, self.district_model), FullTextSearch(text, self.city_model))).all()
        result["district"] = [{"district_name" : district.name, "_id" : district.id, "city_name" : district.city.name} for district in districts]
        return result

    def get_address_search_result(self, result, text):
        addresses = self.session.query(
                                self.address_model
                                        ).join(
                                            self.district_model, self.address_model.district_id == self.district_model.id
                                        ).join(
                                            self.city_model, self.district_model.city_id == self.city_model.id
                                        ).filter(or_(
                                            FullTextSearch(text, self.address_model), 
                                            FullTextSearch(text, self.district_model), 
                                            FullTextSearch(text, self.city_model))).all()
        result["address"] = [{"address_detail" : address.detail, "_id" : address.id, "district_name" : address.district.name, "city_name" : address.district.city.name} for address in addresses]
        return result

    def get_store_search_result(self, result, text):
        stores = self.session.query(
                                self.store_model
                                        ).join(
                                            self.address_model, self.store_model.address_id == self.address_model.id
                                        ).join(
                                            self.district_model, self.address_model.district_id == self.district_model.id
                                        ).join(
                                            self.city_model, self.district_model.city_id == self.city_model.id
                                        ).filter(or_(
                                            FullTextSearch(text, self.address_model), 
                                            FullTextSearch(text, self.store_model), 
                                            FullTextSearch(text, self.district_model), 
                                            FullTextSearch(text, self.city_model))).all()
        result["store"] = [{"store_name" : store.store_name, "_id" : store.id, "address_detail" : store.address.detail, "district_name" : store.address.district.name, "city_name" : store.address.district.city.name} for store in stores]
        return result

    def get_color_search_result(self, result, text):
        colors = self.session.query(
                        self.color_model
                                ).filter(FullTextSearch(text, self.color_model, FullTextMode.BOOLEAN)).all()

        result["color"] = [{"color_value" : color.value, "_id" : color.id} for color in colors]
        return result

    def get_brand_search_result(self, result, text):
        brands = self.session.query(
                        self.brand_model
                                ).filter(FullTextSearch(text, self.brand_model, FullTextMode.BOOLEAN)).all()
        result["brand"] = [{"brand_name" : brand.name, "_id" : brand.id} for brand in brands]
        return result

    def get_product_search_result(self, result, text):
        products = self.session.query(
                                self.product_model
                                        ).join(
                                            self.category_model, self.product_model.category_id == self.category_model.id
                                        ).join(
                                            self.brand_model, self.category_model.brand_id == self.brand_model.id
                                        ).filter(or_(
                                            FullTextSearch(text, self.product_model), 
                                            FullTextSearch(text, self.category_model), 
                                            FullTextSearch(text, self.brand_model))).all()
        result["product"] = [{"product_detail" : product.detail, "_id" : product.id, "category_name" : product.category.name, "brand_name" : product.category.brand.name} for product in products]
        return result


    def get_category_search_result(self, result, text):
        categories = self.session.query(self.category_model).join(self.brand_model, self.category_model.brand_id == self.brand_model.id).filter(or_(FullTextSearch(text, self.category_model), FullTextSearch(text, self.brand_model))).all()
        result["category"] = [{"category_name" : category.name, "_id" : category.id, "brand_name" : category.brand.name} for category in categories]
        return result


    def get_variant_search_result(self, result, text):
        variants = self.session.query(
                                self.model
                                        ).join(
                                            self.product_model, self.model.product_id == self.product_model.id
                                        ).join(
                                            self.store_model, self.model.store_id == self.store_model.id
                                        ).join(
                                            self.color_model, self.model.color_id == self.color_model.id
                                        ).join(
                                            self.category_model, self.product_model.category_id == self.category_model.id
                                        ).join(
                                            self.brand_model, self.category_model.brand_id == self.brand_model.id
                                        ).join(
                                            self.address_model, self.store_model.address_id == self.address_model.id
                                        ).join(
                                            self.district_model, self.address_model.district_id == self.district_model.id
                                        ).join(
                                            self.city_model, self.district_model.city_id == self.city_model.id
                                        ).filter(
                                            or_(
                                                FullTextSearch(text, self.product_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.category_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.brand_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.store_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.address_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.district_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.city_model, FullTextMode.BOOLEAN),
                                                FullTextSearch(text, self.color_model, FullTextMode.BOOLEAN)
                                            )
                                        ).all()
        result["variant"] = [{"variant_price" : variant.price, "_id" : variant.id, 
                "product_name" : variant.product.name, "category_name" : variant.product.category.name,
                "brand_name" : variant.product.category.brand.name, "color_value" : variant.color.value,
                "store_name" : variant.store.store_name, "address_detail" : variant.store.address.detail,
                "district_name" : variant.store.address.district.name, 
                "city_name" : variant.store.address.district.city.name} for variant in variants]

        return result

    def check_or_create_session(self):
        if not hasattr(self, "session"):
            engine = self.db.engine
            Session = sessionmaker(bind=engine)
            self.session = Session()
