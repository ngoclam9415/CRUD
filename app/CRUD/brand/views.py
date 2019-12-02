from flask import Blueprint, render_template, request, make_response, jsonify, redirect, flash

from database import access_factory
from unidecode import unidecode

brand_blueprint = Blueprint('brand', __name__, template_folder='templates')


@brand_blueprint.route('/api/list', methods=['GET'])
def list_brand_api():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("brand").list_item(page=page)
    return make_response(jsonify(res), 200)


@brand_blueprint.route('/', methods=['GET'])
def list_brand():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("brand").list_item(page=page)    
    return render_template('CRUD/brand/list.html', total_pages=res["total_pages"], brand_active="active")


@brand_blueprint.route('/create', methods=['GET', 'POST'])
def create_brand(error=None):
    if request.method == 'POST':
        brand_name = request.form['brandName']
        if access_factory.get_access("brand").verify_qualified_item(name=brand_name) and brand_name != "":
            no_accent = unidecode(brand_name)
            access_factory.get_access("brand").create_item(name=brand_name, no_accent=no_accent.lower())
            return redirect('/brand')
        else:
            error = "Your brand is error"
    return render_template('CRUD/brand/create.html', error=error, brand_active="active")


@brand_blueprint.route('/edit', methods=['POST'])
def edit_brand():
    brand_id = request.form['brand_id']
    brand_name = request.form['brand_name']
    if brand_name != "" and access_factory.get_access("brand").verify_qualified_item(name=brand_name):
        no_accent = unidecode(brand_name)
        access_factory.get_access("brand").edit_item(brand_id, name=brand_name, no_accent=no_accent.lower())
    else :
        flash("INPUT BRAND INVALID", "error")
    return redirect('/brand')
