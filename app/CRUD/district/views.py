from flask import Blueprint, render_template, current_app, request, jsonify
from app.models import *
from app import db
district_blueprint = Blueprint('district', __name__, template_folder='templates')


@district_blueprint.route('/', methods=['GET'])
def district():
    infos = [{"id" : 1, "city" : "Ho Chi Minh", "name" : "Quan 2"},
        {"id" : 2, "city" : "Ho Chi Minh", "name" : "Binh Thanh"},
        {"id" : 3, "city" : "Ho Chi Minh", "name" : "Quan 7"}]
    cities = ["Ho Chi Minh", "Ha Noi", "Quy Nhon", "Da Nang"]
    results = City.query.all()
    cities = [result.name for result in results]
    results = District.query.all()
    infos = [{"id" : result.id, "name" : result.name, "city" : result.city.name} for result in results]
    return render_template('CRUD/district/district.html', infos=infos, district_active="active", cities=cities)


@district_blueprint.route('/create', methods=['POST'])
def create_district():
    data = request.get_json()
    district_name = data.get("district_name", None)
    city_name = data.get("city_name", None)
    if district_name is None or city_name is None:
        return jsonify({"sucess" : False, "data" : None})
    city = City.query.filter(City.name==city_name).first()
    district = District(name=district_name, city=city)
    db.session.add(district)
    db.session.commit()
    data = {"id" : district.id, "name": district.name, "city": city_name}
    return jsonify({"sucess" : True, "data" : data})
    
@district_blueprint.route('/edit', methods=['POST'])
def edit_district():
    data = request.get_json()
    district_id = data.get("district_id", None)
    district_name = data.get("district_name", None)
    city_name = data.get("city_name", None)
    if district_name is None or city_name is None or district_id is None:
        return jsonify({"sucess" : False, "data" : None})
    district = District.query.filter(District.id==district_id).first()
    district.name = district_name
    district.city.name = city_name
    # district.city = city
    db.session.commit()
    data = {"id" : district.id, "name": district.name, "city": city_name}
    return jsonify({"sucess" : True, "data" : data})