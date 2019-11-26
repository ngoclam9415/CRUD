from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, flash
from database import access_factory

search_blueprint = Blueprint(
    'search', __name__, template_folder='templates')


@search_blueprint.route('/', methods=['GET'])
def index():
    search_info = request.values.get("search", None)
    data = {}
    if search_info != "" and search_info is not None:
        data = access_factory.get_access("search").show_searched_item(search_info)
    return render_template("CRUD/search/search.html", 
                    cities=data.get("city", []),
                    districts=data.get("district", []),
                    addresses=data.get("address", []),
                    stores=data.get("store", []),
                    colors=data.get("color", []),
                    brands=data.get("brand", []),
                    categories=data.get("category", []),
                    products=data.get("product", []),
                    variants=data.get("variant", []))
    