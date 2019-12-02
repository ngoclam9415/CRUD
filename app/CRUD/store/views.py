from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, flash
from database.mysql_access.models import db
from database import access_factory
from unidecode import unidecode

store_blueprint = Blueprint(
    'store', __name__, template_folder='templates')


@store_blueprint.route('/', methods=['GET'])
def index():
    page = request.args.get("page", 1, type=int)
    addresses = access_factory.get_access("store").get_addresses()
    res = access_factory.get_access("store").list_item(page=page)
    return render_template('CRUD/store/index.html', addresses=addresses, store_active="active", stores=res["data"], pages=res["total_pages"])


@store_blueprint.route('/api/create', methods=['POST'])
def api_create():
    data = request.values
    store_name = data.get("store_name", None)
    address_id = data.get("address_id", None)
    if store_name is None or address_id is None or not access_factory.get_access("store").verify_qualified_item(store_name=store_name, address_id=address_id):
        flash("STORE INPUT INVALID", "error")
        return redirect(url_for("store.index"))
    no_accent = unidecode(store_name)
    access_factory.get_access("store").create_item(store_name=store_name, address_id=address_id, no_accent=no_accent.lower())
    return redirect(url_for("store.index"))


@store_blueprint.route('/api/edit', methods=['POST'])
def api_edit():
    data = request.get_json()
    id = data.get("id", None)
    name = data.get("name", None)
    address_id = data.get("address_id", None)
    if name is None or address_id is None or id is None or not access_factory.get_access("store").verify_qualified_item(store_name=name, address_id=address_id):
        return jsonify({"sucess": False, "data": None})
    no_accent = unidecode(name)
    access_factory.get_access("store").edit_item(id, store_name=name, address_id=address_id, no_accent=no_accent.lower())
    return jsonify({"sucess": True})


@store_blueprint.route("/create")
def create():
    addresses = access_factory.get_access("store").get_addresses()
    return render_template("CRUD/store/create.html", addresses=addresses, store_active="active")
