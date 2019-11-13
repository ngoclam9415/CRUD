from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for
from app.models import City, District
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
    return render_template('CRUD/district/district.html', infos=results.items, district_active="active", cities=cities, pages=results.pages)


@district_blueprint.route('/api/create', methods=['POST'])
def create_district():
    data = request.values
    district_name = data.get("district_name", None)
    city_id = data.get("city_id", None)
    if district_name is None or city_id is None:
        return jsonify({"sucess": False, "data": None})
    district = District(name=district_name, city_id=city_id)
    db.session.add(district)
    db.session.commit()
    return redirect(url_for("district.district"))


@district_blueprint.route('/api/edit', methods=['POST'])
def edit_district():
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


@district_blueprint.route("/create")
def test():
    cities = City.query.all()
    return render_template("CRUD/district/create.html", cities=cities, district_active="active")
