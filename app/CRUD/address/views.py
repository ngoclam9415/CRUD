from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import District, City, Address
from app import db

address_blueprint = Blueprint('address', __name__, template_folder='templates')


@address_blueprint.route('/create', methods=['POST', 'GET'])
def create_address():
    if request.method == 'POST':
        district_id = request.form.get('select-district')
        detail = request.form.get('address')

        if not district_id or not detail:
            flash('Vui lòng nhập lại thông tin', 'error')
            return redirect(url_for('address.create_address'))

        new_address = Address(district_id=district_id,  detail=detail)

        db.session.add(new_address)
        db.session.commit()
        return redirect(url_for('address.list_addresses'))

    list_city = [city for city in City.query.all()]

    return render_template('CRUD/address/create.html', list_city=list_city, address_active="active")


@address_blueprint.route('/district', methods=['GET'])
def get_district_by_city():
    city_id = request.args.get('city_id')
    if not city_id:
        return jsonify({})

    districts = District.query.filter_by(city_id=city_id).all()

    jsonable_district = [{'id': district.id, 'name': district.name}
                         for district in districts]
    return jsonify(jsonable_district)


@address_blueprint.route('/', methods=['GET'])
def list_addresses():
    page = request.args.get("page", 1, type=int)

    addresses_pagination = Address.query.order_by(
        Address.id).paginate(page=page, per_page=10, error_out=False)

    total_page = addresses_pagination.pages
    current_page = addresses_pagination.page

    addresses = [{'city': address.district.city.name, 'city_id': address.district.city.id,
                  'district': address.district.name, 'district_id': address.district.id,
                  'detail': address.detail, 'id': address.id}
                 for address in addresses_pagination.items]

    list_city = [city for city in City.query.all()]

    return render_template('CRUD/address/show-address.html', addresses=addresses, total_page=total_page, current_page=current_page, list_city=list_city, address_active="active")


@address_blueprint.route('/edit', methods=['POST'])
def edit_address():
    new_address_info = request.get_json()

    db.session.query(Address).filter(
        Address.id == new_address_info.get('address_id', None)).update(
            {
                "district_id": new_address_info.get('district_id'),
                "detail": new_address_info.get('address_detail'),
            }
    )

    db.session.commit()

    return jsonify({"status": "ok"})
