from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for
from app.models import City, District, Address, Store
from app import db
from app.utils import page_number_caculater

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route('/', methods=['GET'])
def index():
    per_page = 10
    page = request.args.get("page", 1, type=int)
    addresses = Address.query.order_by(Address.id).all()
    stores = Store.query.paginate(page, per_page, error_out=False)
    return render_template('CRUD/store/index.html', addresses=addresses, store_active="active", stores=stores.items, pages=stores.pages)


@store_blueprint.route('/api/create', methods=['POST'])
def api_create():
    # print(request.values)
    data = request.values
    store_name = data.get("store_name", None)
    address_id = data.get("address_id", None)
    if store_name is None or address_id is None:
        return jsonify({"sucess": False, "data": None})
    store = Store(store_name=store_name, address_id=address_id)
    db.session.add(store)
    db.session.commit()
    return redirect(url_for("store.index"))


@store_blueprint.route('/api/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    district_id = data.get("district_id", None)
    district_name = data.get("district_name", None)
    city_id = data.get("city_id", None)
    if district_name is None or city_id is None or district_id is None:
        return jsonify({"sucess": False, "data": None})
    district = District.query.filter(District.id == district_id).first()
    district.name = district_name
    district.city_id = city_id
    db.session.commit()
    data = {"id": district.id, "name": district.name, "city": city_id}
    return jsonify({"sucess": True, "data": data})


@store_blueprint.route("/create")
def create():
    addresses = Address.query.all()
    return render_template("CRUD/store/create.html", addresses=addresses)
