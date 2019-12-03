from database.mysql_access.base_class.BaseDataAccess import BaseDataAccess
from config import PageConfig as config
import math
from database.mongo_access.base_class.BaseLogicModel import BaseLogicModel as searcher
from database.search_engine.elastic_search import ElasticEngine
import re

class SearchDataAccess(ElasticEngine):
    def __init__(self, *args, ip="localhost", port=9200):
        super(SearchDataAccess, self).__init__(ip, port)

    def show_searched_item(self, text):
        results = super(SearchDataAccess, self).fuzzy_search_index("_all", text)
        if len(results["hits"]["hits"]) and "highlight" in results["hits"]["hits"][0].keys():
            matched = results["hits"]["hits"][0]["highlight"]["no_accent"][0]
            matched_string = re.search(r"<em>(.*)<\/em>", matched).group(1)
            return_dict = searcher("Search").show_searched_item(matched_string)
        else:
            return_dict = {}
            for result in results["hits"]["hits"]:
                return_dict.setdefault(result["_index"], [])
                result["_source"]["_id"] = str(result["_id"])
                if result["_index"] in ["city", "district", "brand", "category", "product"]:
                    sub_fix = result["_index"] + "_name"
                    result["_source"][sub_fix] = result["_source"]["name"]
                elif result["_index"] == "color":
                    sub_fix = result["_index"] + "_value"
                    result["_source"][sub_fix] = result["_source"]["value"]
                elif result["_index"] == "store":
                    sub_fix = result["_index"] + "_name"
                    result["_source"][sub_fix] = result["_source"]["store_name"]
                elif result["_index"] == "address":
                    sub_fix = result["_index"] + "_detail"
                    result["_source"][sub_fix] = result["_source"]["detail"]
                elif result["_index"] == "variant":
                    sub_fix = result["_index"] + "_price"
                    result["_source"][sub_fix] = result["_source"]["price"]
                return_dict[result["_index"]].append(result["_source"])
        return return_dict

    def suggest_item(self, text):
        results = super(SearchDataAccess, self).suggestion_search_index("_all", text)
        return_list = []
        for result in results["hits"]["hits"]:
            for key, val in result["_source"].items():
                if key in ["name", "store_name", "price", "detail", "value"]:
                    return_list.append(val)
        return return_list