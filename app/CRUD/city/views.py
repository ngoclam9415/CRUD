from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import db
from app.models import City

city_blueprint = Blueprint('city', __name__, template_folder='templates')


@city_blueprint.route('/api/list', methods=['GET'])
def list_city_api():
    page = request.args.get('page', 1, type=int)
    cities = City.query.order_by(City.id).paginate(page, 10, error_out=False)
    total_pages = cities.pages
    arr_city = []
    for city in cities.items:
        tmp_city = {
            'id': city.id,
            'name': city.name
        }
        arr_city.append(tmp_city)
    res = {
        "total_pages": total_pages,
        "data": arr_city,
    }
    return make_response(jsonify(res), 200)


@city_blueprint.route('/', methods=['GET'])
def list_city():
    page = request.args.get('page', 1, type=int)
    cities = City.query.order_by(City.id).paginate(page, 10, error_out=False)
    total_pages = cities.pages
    return render_template('CRUD/city/list.html', total_pages=total_pages, city_active="active")


@city_blueprint.route('/create', methods=['GET', 'POST'])
def create_city(error=None):
    if request.method == 'POST':
        city_name = request.form['cityName']
        city_exist = City.query.filter_by(name=city_name).first()
        if city_exist is None and city_name != "":
            new_city = City(name=city_name)
            db.session.add(new_city)
            db.session.commit()
            return redirect('/city')
        else:
            error = "Your city is error"
    return render_template('CRUD/city/create.html', error=error, city_active="active")


@city_blueprint.route('/edit', methods=['POST'])
def edit_city():
        city_id = request.form['city_id']
        city_name = request.form['city_name']
        db.session.query(City).filter(City.id == city_id).update({"name": city_name})
        db.session.commit()
        return redirect('/city')
