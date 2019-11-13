from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from app import db
from app.models import City, Category, Brand, Product

product_blueprint = Blueprint('product', __name__, template_folder='templates')


@product_blueprint.route('/api/list', methods=['GET'])
def list_product_api():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page, 10, error_out=False)
    total_pages = products.pages
    arr_product = []
    for product in products.items:
        tmp_product = {
            'id': product.id,
            'name': product.name,
            'category_name': Category.query.get_or_404(int(product.category_id)).name
        }
        arr_product.append(tmp_product)
    res = {
        "total_pages": total_pages,
        "data": arr_product,
    }
    return make_response(jsonify(res), 200)


@product_blueprint.route('/', methods=['GET'])
def list_product():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page, 10, error_out=False)
    total_pages = products.pages
    categories = Category.query.all()
    return render_template('CRUD/product/list.html', total_pages=total_pages, categories=categories, product_active="active")


@product_blueprint.route('/create', methods=['GET', 'POST'])
def create_product(error=None):
    categories = Category.query.all()
    if request.method == 'POST':
        product_name = request.form['product_name']
        category_id = request.form['category_id']
        product_exist = Category.query.filter_by(name=product_name).first()
        if product_exist is None and product_name != "":
            new_product = Product(name=product_name, category_id=category_id)
            db.session.add(new_product)
            db.session.commit()
            return redirect('/product')
        else:
            error = "Your product is error"
    return render_template('CRUD/product/create.html', categories=categories, error=error, product_active="active")


@product_blueprint.route('/edit', methods=['POST'])
def edit_product():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    category_id = request.form['category_id']
    db.session.query(Product).filter(Product.id == product_id).update({"name": product_name, "category_id": int(category_id)})
    db.session.commit()
    return redirect('/product')
