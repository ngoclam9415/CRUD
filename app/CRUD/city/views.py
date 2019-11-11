from flask import Blueprint, render_template

city_blueprint = Blueprint('city', __name__, template_folder='templates')


@city_blueprint.route('/create', methods=['GET'])
def city():
    return render_template('CRUD/city/create.html')
