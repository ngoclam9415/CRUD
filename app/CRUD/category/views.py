from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import db
from app.models import City, Category, Brand

category_blueprint = Blueprint('category', __name__, template_folder='templates')


@category_blueprint.route('/api/list', methods=['GET'])
def list_category_api():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page, 10, error_out=False)
    total_pages = categories.pages
    arr_category = []
    for category in categories.items:
        tmp_category = {
            'id': category.id,
            'name': category.name,
            'brand_name': Brand.query.get_or_404(int(category.brand_id)).name
        }
        arr_category.append(tmp_category)
    res = {
        "total_pages": total_pages,
        "data": arr_category,
    }
    return make_response(jsonify(res), 200)


@category_blueprint.route('/', methods=['GET'])
def list_category():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page, 10, error_out=False)
    total_pages = categories.pages
    brands = Brand.query.all()
    return render_template('CRUD/category/list.html', total_pages=total_pages, brands=brands, category_active="active")


@category_blueprint.route('/create', methods=['GET', 'POST'])
def create_category(error=None):
    brands = Brand.query.all()
    if request.method == 'POST':
        category_name = request.form['category_name']
        brand_id = request.form['brand_id']
        category_exist = Category.query.filter_by(name=category_name).first()
        if category_exist is None and category_name != "":
            new_category = Category(name=category_name, brand_id=brand_id)
            db.session.add(new_category)
            db.session.commit()
            return redirect('/category')
        else:
            error = "Your category is error"
    return render_template('CRUD/category/create.html', brands=brands, error=error, category_active="active")


@category_blueprint.route('/edit', methods=['POST'])
def edit_category():
    category_id = request.form['category_id']
    category_name = request.form['category_name']
    brand_id = request.form['brand_id']
    db.session.query(Category).filter(Category.id == category_id).update({"name": category_name, "brand_id": int(brand_id)})
    db.session.commit()
    return redirect('/category')
