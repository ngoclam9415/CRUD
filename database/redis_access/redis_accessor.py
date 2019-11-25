import redis
import json
import pickle

class RedisAccessor:
    def __init__(self, redis_cli):
        self.redis_cli = redis_cli
        #TODO FINISH THIS

    def save(self, key, dict_data):
        serialized_data = pickle.dumps(dict_data)
        flag = self.redis_cli.set(key, serialized_data)
        return flag

    def load(self, key):
        serialized_data = self.redis_cli.get(key)
        if serialized_data is None:
            return None
        # serialized_data = serialized_data.decode()
        dict_data = pickle.loads(serialized_data)
        return dict_data

    def modify(self, key, **kwargs):
        dict_data = self.load(key)
        dict_data.update(kwargs)
        flag = self.save(key, dict_data)
        return flag

    def exist(self, key):
        return self.redis_cli.exists(key)


