from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import db
from app.models import Brand

brand_blueprint = Blueprint('brand', __name__, template_folder='templates')


@brand_blueprint.route('/api/list', methods=['GET'])
def list_brand_api():
    page = request.args.get('page', 1, type=int)
    cities = Brand.query.paginate(page, 10, error_out=False)
    total_pages = cities.pages
    arr_brand = []
    for brand in cities.items:
        tmp_brand = {
            'id': brand.id,
            'name': brand.name
        }
        arr_brand.append(tmp_brand)
    res = {
        "total_pages": total_pages,
        "data": arr_brand,
    }
    return make_response(jsonify(res), 200)


@brand_blueprint.route('/', methods=['GET'])
def list_brand():
    page = request.args.get('page', 1, type=int)
    cities = Brand.query.paginate(page, 10, error_out=False)
    total_pages = cities.pages
    return render_template('CRUD/brand/list.html', total_pages=total_pages, brand_active="active")


@brand_blueprint.route('/create', methods=['GET', 'POST'])
def create_brand(error=None):
    if request.method == 'POST':
        brand_name = request.form['brandName']
        brand_exist = Brand.query.filter_by(name=brand_name).first()
        if brand_exist is None and brand_name != "":
            new_brand = Brand(name=brand_name)
            db.session.add(new_brand)
            db.session.commit()
            return redirect('/brand')
        else:
            error = "Your brand is error"
    return render_template('CRUD/brand/create.html', error=error, brand_active="active")


@brand_blueprint.route('/edit', methods=['POST'])
def edit_brand():
    brand_id = request.form['brand_id']
    brand_name = request.form['brand_name']
    db.session.query(Brand).filter(
        Brand.id == brand_id).update({"name": brand_name})
    db.session.commit()
    return redirect('/brand')
