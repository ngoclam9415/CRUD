from database.mongo_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
from bson.objectid import ObjectId
import json

class ProductVariantDataAccess:
    def __init__(self, db, variant_col, product_col, )