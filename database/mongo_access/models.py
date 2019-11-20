import pymongo
from config import MongoDBConfig as config

class BaseModel:
    def __init__(self):
        self.mongodb = pymongo.MongoClient(host=config.IP, port=config.PORT)
        self.db = self.mongodb["product"]

    def add_collection(self, col_name):
        return self.db[col_name]
        
    def init_app(self, app):
        print("HELLO APP")

db = BaseModel()