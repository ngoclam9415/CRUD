from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, flash
from database import access_factory

variant_blueprint = Blueprint(
    'variant', __name__, template_folder='templates')


@variant_blueprint.route('/', methods=['GET'])
def index():

    page = request.args.get("page", 1, type=int)
    stores = access_factory.get_access("variant").get_stores()
    products = access_factory.get_access("variant").get_products()
    colors = access_factory.get_access("variant").get_colors()
    res = access_factory.get_access("variant").list_item(page=page)
    return render_template('CRUD/product_variant/index.html', stores=stores, products=products, colors=colors, variant_active="active", variants=res["data"], pages=res["total_pages"])


@variant_blueprint.route('/api/create', methods=['POST'])
def api_create():
    price = request.values.get("product_variant_price", 0, type=int)
    product_id = request.values.get("product_id", None)
    store_id = request.values.get("store_id", None)
    color_id = request.values.get("color_id", None)

    if not product_id or not store_id or not color_id or not access_factory.get_access("variant").verify_qualified_item(product_id=product_id, store_id=store_id, color_id=color_id):
        flash("PRODUCT VARIANT INPUT INVALID", "error")
        redirect(url_for("variant.index"))
    access_factory.get_access("variant").create_item(price=price, product_id=product_id, store_id=store_id, color_id=color_id)
    return redirect(url_for("variant.index"))


@variant_blueprint.route('/api/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    id = data.get("id", None)
    price = data.get("price", None)
    product_id = data.get("product_id", None)
    store_id = data.get("store_id", None)
    color_id = data.get("color_id", None)

    if product_id is None or store_id is None or id is None or color_id is None or not access_factory.get_access("variant").verify_qualified_item(price=price, product_id=product_id, store_id=store_id, color_id=color_id):
        return jsonify({"sucess": False, "data": None})

    access_factory.get_access("variant").edit_item(id, price=price, product_id=product_id, store_id=store_id, color_id=color_id)
    return jsonify({"sucess": True})


@variant_blueprint.route("/create")
def create():
    stores = access_factory.get_access("variant").get_stores()
    products = access_factory.get_access("variant").get_products()
    colors = access_factory.get_access("variant").get_colors()
    return render_template("CRUD/product_variant/create.html", stores=stores, products=products, colors=colors)
