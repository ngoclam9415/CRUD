from flask import Blueprint, render_template, request

address_blueprint = Blueprint('address', __name__, template_folder='templates')


@address_blueprint.route('/create', methods=['GET', 'POST'])
def create_address():
    if request.method == 'POST':
    return render_template('CRUD/address/create.html')
