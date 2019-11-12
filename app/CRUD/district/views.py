from flask import Blueprint, render_template, current_app, request, jsonify
from app.models import *
from app import db
from app.utils import page_number_caculater

district_blueprint = Blueprint(
    'district', __name__, template_folder='templates')


@district_blueprint.route('/', methods=['GET'])
def district():
    per_page = 10
    page = request.args.get("page", 1, type=int)
    cities = City.query.all()
    results = District.query.paginate(page, per_page, error_out=False)
    infos = [{"id": result.id, "name": result.name, "city": result.city.name}
             for result in results.items]
    return render_template('CRUD/district/district.html', infos=infos, district_active="active", cities=cities, pages=results.pages)


@district_blueprint.route('/api/create', methods=['POST'])
def create_district():
    data = request.get_json()
    district_name = data.get("district_name", None)
    city_name = data.get("city_name", None)
    if district_name is None or city_name is None:
        return jsonify({"sucess": False, "data": None})
    city = City.query.filter(City.name == city_name).first()
    district = District(name=district_name, city=city)
    db.session.add(district)
    db.session.commit()
    data = {"id": district.id, "name": district.name, "city": city_name}
    return jsonify({"sucess": True, "data": data})


@district_blueprint.route('/api/edit', methods=['POST'])
def edit_district():
    data = request.get_json()
    district_id = data.get("district_id", None)
    district_name = data.get("district_name", None)
    city_name = data.get("city_name", None)
    if district_name is None or city_name is None or district_id is None:
        return jsonify({"sucess": False, "data": None})
    district = District.query.filter(District.id == district_id).first()
    district.name = district_name
    district.city.name = city_name
    # district.city = city
    db.session.commit()
    data = {"id": district.id, "name": district.name, "city": city_name}
    return jsonify({"sucess": True, "data": data})


@district_blueprint.route("/test")
def test():
    return render_template("CRUD/district/create.html")
