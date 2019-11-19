from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for

from database.mysql_access.models import db
from database.mysql_access.models import City, Category, Brand
from database import access_factory

category_blueprint = Blueprint('category', __name__, template_folder='templates')


@category_blueprint.route('/api/list', methods=['GET'])
def list_category_api():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("category").list_item(page=page)
    return make_response(jsonify(res), 200)


@category_blueprint.route('/', methods=['GET'])
def list_category():
    error = request.args.get("error", None)
    print(error)
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("category").list_item(page=page)
    return render_template('CRUD/category/list.html', total_pages=res["total_pages"], brands=res["brands"], category_active="active", error=error)


@category_blueprint.route('/create', methods=['GET', 'POST'])
def create_category(error=None):
    brands = Brand.query.all()
    if request.method == 'POST':
        category_name = request.form['category_name']
        brand_id = request.form['brand_id']
        if category_name != "" and access_factory.get_access("category").verify_qualified_item(name=category_name, brand_id=brand_id) :
            access_factory.get_access("category").create_item(name=category_name, brand_id=brand_id)
            return redirect('/category')
        else:
            error = "Your category is error"
    return render_template('CRUD/category/create.html', brands=brands, error=error, category_active="active")


@category_blueprint.route('/edit', methods=['POST'])
def edit_category():
    category_id = request.form.get('category_id', type=int)
    category_name = request.form['category_name']
    brand_id = request.form.get('brand_id', type=int)
    if category_name != "" and access_factory.get_access("category").verify_qualified_item(name=category_name, brand_id=brand_id):
        access_factory.get_access("category").edit_item(category_id, name=category_name, brand_id=brand_id)
    else:
        return redirect(url_for("category.list_category", error="EDIT INPUT INVALID"))
    return redirect('/category')
