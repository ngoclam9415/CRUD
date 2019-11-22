from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from database.mysql_access.models import District, City, Address
from database.mysql_access.models import db
from database import access_factory

address_blueprint = Blueprint('address', __name__, template_folder='templates')


@address_blueprint.route('/create', methods=['POST', 'GET'])
def create_address():
    if request.method == 'POST':
        district_id = request.form.get('select-district')
        detail = request.form.get('address')
        if not district_id or not detail or not access_factory.get_access("address").verify_qualified_item(district_id=district_id,  detail=detail):
            flash('Vui lòng nhập lại thông tin', 'error')
            return redirect(url_for('address.create_address'))
        access_factory.get_access("address").create_item(district_id=district_id,  detail=detail)
        return redirect(url_for('address.list_addresses'))
    list_city = access_factory.get_access("address").get_cities()
    return render_template('CRUD/address/create.html', list_city=list_city, address_active="active")


@address_blueprint.route('/district', methods=['GET'])
def get_district_by_city():
    city_id = request.args.get('city_id')
    if not city_id:
        return jsonify({})
    districts = access_factory.get_access("address").get_districts_by_city(city_id=city_id)
    return jsonify(districts)


@address_blueprint.route('/', methods=['GET'])
def list_addresses():
    page = request.args.get("page", 1, type=int)
    res = access_factory.get_access("address").list_item(page=page)
    list_city = access_factory.get_access("address").get_cities()
    return render_template('CRUD/address/show-address.html', addresses=res["addresses"], total_page=res["total_page"], current_page=page, list_city=list_city, address_active="active")


@address_blueprint.route('/edit', methods=['POST'])
def edit_address():
    new_address_info = request.get_json()
    address_id = new_address_info.get('address_id', None)
    district_id = new_address_info.get('district_id')
    detail = new_address_info.get('address_detail')
    if detail != "" and access_factory.get_access("address").verify_qualified_item(district_id=district_id, detail=detail):
        access_factory.get_access("address").edit_item(address_id, district_id=district_id, detail=detail)
    return jsonify({"status": "ok"})
