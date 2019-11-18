from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for
from database.mysql_access.models import City, District
from database.mysql_access.models import db
from database import access_factory

district_blueprint = Blueprint(
    'district', __name__, template_folder='templates')


@district_blueprint.route('/', methods=['GET'])
def district():
    page = request.args.get("page", 1, type=int)
    res = access_factory.get_access("district").list_item(page=page)
    return render_template('CRUD/district/district.html', infos=res["infos"], district_active="active", cities=res["cities"], pages=res["pages"])


@district_blueprint.route('/api/create', methods=['POST'])
def create_district():
    data = request.values
    district_name = data.get("district_name", None)
    city_id = data.get("city_id", None)
    if access_factory.get_access("district").verify_qualified_item(name=district_name, city_id=city_id) and district_name != "":
        access_factory.get_access("district").create_item(name=district_name, city_id=city_id)
    else:
        return jsonify({"success": False, "data": None})
    return redirect(url_for("district.district"))


@district_blueprint.route('/api/edit', methods=['POST'])
def edit_district():
    data = request.get_json()
    district_id = data.get("district_id", None)
    district_name = data.get("district_name", None)
    city_id = data.get("city_id", None)
    if district_name is None or city_id is None or district_id is None or not access_factory.get_access("district").verify_qualified_item(name=district_name, city_id=city_id):
        return jsonify({"success": False, "data": None})
    access_factory.get_access("district").edit_item(district_id, name=district_name, city_id=city_id)
    return jsonify({"success": True})


@district_blueprint.route("/create")
def test():
    cities = City.query.all()
    return render_template("CRUD/district/create.html", cities=cities, district_active="active")
