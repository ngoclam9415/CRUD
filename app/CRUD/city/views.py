from flask import Blueprint, render_template, request, make_response, jsonify, redirect, flash

from database import access_factory

city_blueprint = Blueprint('city', __name__, template_folder='templates')


@city_blueprint.route('/api/list', methods=['GET'])
def list_city_api():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("city").list_item(page=page)
    return make_response(jsonify(res), 200)


@city_blueprint.route('/', methods=['GET'])
def list_city():
    page = request.args.get('page', 1, type=int)
    res = access_factory.get_access("city").list_item(page=page)
    return render_template('CRUD/city/list.html', total_pages=res["total_pages"], city_active="active")


@city_blueprint.route('/create', methods=['GET', 'POST'])
def create_city(error=None):
    if request.method == 'POST':
        city_name = request.form['cityName']
        if access_factory.get_access("city").verify_qualified_item(name=city_name) and city_name != "":
            access_factory.get_access("city").create_item(name=city_name)
            return redirect('/city')
        else:
            error = "Your city is error"
    return render_template('CRUD/city/create.html', error=error, city_active="active")


@city_blueprint.route('/edit', methods=['POST'])
def edit_city():
        city_id = request.form['city_id']
        city_name = request.form['city_name']
        if city_name != "" and access_factory.get_access("city").verify_qualified_item(name=city_name):
            access_factory.get_access("city").edit_item(city_id, name=city_name)
        else:
            flash("CITY INPUT INVALID", "error")
        return redirect('/city')
