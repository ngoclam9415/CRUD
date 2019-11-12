from flask import Blueprint, render_template, request
from app.models import District, City

address_blueprint = Blueprint('address', __name__, template_folder='templates')


@address_blueprint.route('/create', methods=['POST'])
def create_address():

    return render_template('CRUD/address/create.html')


@address_blueprint.route('/create', methods=['GET'])
def create_show_address():

    list_city = [city.name for city in City.query.all()]
    list_district = [district.name for district in District.query.all()]

    return render_template('CRUD/address/create.html', list_city=list_city, list_district=list_district)
