from elasticsearch import Elasticsearch

class ElasticEngine:
    def __init__(self, ip="localhost", port=9200):
        self.searcher = Elasticsearch(hosts=["{}:{}".format(ip, port)])

    def add_to_index(self, index_name, id, data):
        self.searcher.index(index=index_name, id=id, body=data)

    def remove_from_index(self, index_name, id):
        self.searcher.delete(index=index_name, id=id)

    def fulltext_search_index(self, index, query):
        search_result = self.searcher.search(index, body={'query': {'multi_match': {'query': query, 'fields': ['*']}}})
        return search_result

    def fuzzy_search_index(self, index, query):
        search_result = self.searcher.search(index, body={"query": 
            {
                "multi_match": 
                    {
                        "query": query, 
                        "fields": ["*"], 
                        "fuzziness" : "AUTO"
                    }
            }, 
        # "explain" : True,
        "highlight": 
            {
                "fields" : 
                    {
                    "no_accent" : {}
                    }
            }
        })
        return search_result

    def suggestion_search_index(self, index, query):
        body = {
                    "query": {
                        "bool" : {"should" : []}
                    },
                    # "explain" : True,
                    "highlight": {
                            "fields" : {
                                "no_accent" : {}
                            }
                    }
                }
        for i in ["name", "store_name", "value", "detail"]:
            body["query"]["bool"]["should"].append({
                                "match_phrase_prefix" : {
                                    i: {
                                        "query": query,
                                        "slop": 3,
                                        "max_expansions": 50
                                    }
                                }
                        })
        search_result = self.searcher.search(index, body=body)
        return search_result

    

if __name__ == "__main__":
    from database.mongo_access.base_class.BaseLogicModel import BaseLogicModel
    from database.redis_access.redis_accessor import RedisAccessor
    import redis
    import time
    search_engine = ElasticEngine()
    ra = RedisAccessor(redis.Redis())
    # store_model = BaseLogicModel("Store", ra)
    # for store in store_model.list:
    #     data = {}
    #     this_address = ra.load(store["address_id"])
    #     this_district = ra.load(this_address["district_id"])
    #     this_city = ra.load(this_district["city_id"])
    #     data = {"id" : store["id"], 
    #             "store_name" : store["store_name"],
    #             "city_name" : this_city["name"],
    #             "district_name" : this_district["name"],
    #             "address_detail" : this_address["detail"],
    #             "type" : "store"}
    #     search_engine.add_to_index("store", store["id"], data)
    start = time.time()
    search_result = search_engine.suggestion_search_index("_all", "Uni")
    print(time.time() - start)

    print(search_result["hits"]["hits"])