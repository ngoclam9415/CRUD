from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for
from app.models import City, District, Address, ProductVariant, Store, Product, Color
from app import db
from app.utils import page_number_caculater

variant_blueprint = Blueprint(
    'variant', __name__, template_folder='templates')


@variant_blueprint.route('/', methods=['GET'])
def index():

    page = request.args.get("page", 1, type=int)

    stores = Store.query.all()
    products = Product.query.all()
    colors = Color.query.all()

    product_variants = ProductVariant.query.order_by(ProductVariant.id).paginate(
        page=page, per_page=10, error_out=False)

    return render_template('CRUD/product_variant/index.html', stores=stores, products=products, colors=colors, variant_active="active", variants=product_variants.items, pages=product_variants.pages)


@variant_blueprint.route('/api/create', methods=['POST'])
def api_create():
    price = request.values.get("product_variant_price", 0, type=int)
    product_id = request.values.get("product_id", None)
    store_id = request.values.get("store_id", None)
    color_id = request.values.get("color_id", None)

    if not product_id or not store_id or not color_id:
        redirect(url_for("variant.create"))

    new_product_variant = ProductVariant(
        price=price, product_id=product_id, store_id=store_id, color_id=color_id)
    db.session.add(new_product_variant)
    db.session.commit()
    return redirect(url_for("variant.index"))


@variant_blueprint.route('/api/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    id = data.get("id", None)
    price = data.get("price", 0)
    product_id = data.get("product_id", None)
    store_id = data.get("store_id", None)
    color_id = data.get("color_id", None)

    if product_id is None or store_id is None or id is None or color_id is None:
        return jsonify({"sucess": False, "data": None})

    variant = ProductVariant.query.filter(ProductVariant.id == id).first()
    variant.price = price
    variant.product_id = product_id
    variant.store_id = store_id
    variant.color_id = color_id

    db.session.commit()

    return jsonify({"sucess": True})


@variant_blueprint.route("/create")
def create():

    stores = Store.query.all()
    products = Product.query.all()
    colors = Color.query.all()

    return render_template("CRUD/product_variant/create.html", stores=stores, products=products, colors=colors)
