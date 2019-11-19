from flask import Blueprint, render_template, request, make_response, jsonify, redirect, flash

from database.mysql_access.models import db
from database.mysql_access.models import Category, Product
from database import access_factory
product_blueprint = Blueprint('product', __name__, template_folder='templates')


@product_blueprint.route('/api/list', methods=['GET'])
def list_product_api():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("product").list_item(page=page)
    return make_response(jsonify(res), 200)


@product_blueprint.route('/', methods=['GET'])
def list_product():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("product").list_item(page=page)
    categories = access_factory.get_access("product").get_categories()
    return render_template('CRUD/product/list.html', total_pages=res["total_pages"], categories=categories, product_active="active")


@product_blueprint.route('/create', methods=['GET', 'POST'])
def create_product(error=None):
    categories = Category.query.all()
    if request.method == 'POST':
        product_name = request.form['product_name']
        category_id = request.form['category_id']
        if product_name != "" and access_factory.get_access("product").verify_qualified_item(name=product_name, category_id=category_id):
            access_factory.get_access("product").create_item(name=product_name, category_id=category_id)
        else:
            flash("PRODUCT INPUT INVALID", "error")
        return redirect('/product')
    return render_template('CRUD/product/create.html', categories=categories, product_active="active")


@product_blueprint.route('/edit', methods=['POST'])
def edit_product():
    product_id = request.form.get('product_id', None)
    product_name = request.form.get('product_name', None)
    category_id = request.form.get('category_id', None)
    if product_name != "" and access_factory.get_access("product").verify_qualified_item(name=product_name, category_id=category_id):
        access_factory.get_access("product").edit_item(product_id, name=product_name, category_id=category_id)
    else:
        flash("PRODUCT INPUT INVALID", "error")
    return redirect('/product')
