from database import access_factory
import numpy as np
import json


def create_data(parent_col, child_col, added_field, json_file):
    parent_list = access_factory.get_access(parent_col).model.list
    child_list = access_factory.get_access(child_col)
    with open(json_file, 'r') as f:
        list_json = json.load(f)
        for json_item in list_json:
            city = np.random.randint(0, len(parent_list) - 1)
            json_item[added_field] = parent_list[city]["id"]
            child_list.create_item(**dict(json_item))
            print(json_item)

def create_no_relation_data(col, json_file):
    this_col = access_factory.get_access(col)
    with open(json_file, 'r') as f:
        list_json = json.load(f)
        for (i, json_item) in enumerate(list_json):
            this_col.create_item(**dict(json_item))
            print("{}/ Insert : {}".format(i, json_item))

def create_variant():
    products = access_factory.get_access("product").model.list
    stores = access_factory.get_access("store").model.list
    colors = access_factory.get_access("color").model.list
    variants = access_factory.get_access("variant")
    for i in range(1500):
        this_dict = {}
        this_dict["price"] = np.random.randint(500, 10000)
        this_dict["product_id"] = products[np.random.randint(0, len(products) - 1)]["id"]
        this_dict["store_id"] = stores[np.random.randint(0, len(stores) - 1)]["id"]
        this_dict["color_id"] = colors[np.random.randint(0, len(colors) - 1)]["id"]
        variants.create_item(**this_dict)
        print(this_dict)


    
if __name__ == "__main__":
    file_name = "/Users/lam/Downloads/city.json"
    create_no_relation_data("city", file_name)
    file_name = "/Users/lam/Downloads/color.json"
    create_no_relation_data("color", file_name)
    file_name = "/Users/lam/Downloads/brand.json"
    create_no_relation_data("brand", file_name)
    file_name = "/Users/lam/Downloads/district.json"
    create_data("city", "district", "city_id", file_name)
    file_name = "/Users/lam/Downloads/address.json"
    create_data("district", "address", "district_id", file_name)
    file_name = "/Users/lam/Downloads/store.json"
    create_data("address", "store", "address_id", file_name)
    file_name = "/Users/lam/Downloads/category.json"
    create_data("brand", "category", "brand_id", file_name)
    file_name = "/Users/lam/Downloads/product.json"
    create_data("category", "product", "category_id", file_name)
    create_variant()
