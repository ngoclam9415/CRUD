from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for
from app.models import Color
from app import db

color_blueprint = Blueprint(
    'color', __name__, template_folder='templates')


@color_blueprint.route('/', methods=['GET'])
def color():
    per_page = 10
    page = request.args.get("page", 1, type=int)
    colors = Color.query.order_by(Color.id).paginate(page, per_page, error_out=False)
    return render_template('CRUD/color/color.html', color_active="active", colors=colors.items, pages=colors.pages)


@color_blueprint.route('/api/create', methods=['POST'])
def api_create():
    # print(request.values)
    data = request.values
    color_value = data.get("value", None)
    if color_value is None:
        return jsonify({"sucess": False, "data": None})
    color = Color(value=color_value)
    db.session.add(color)
    db.session.commit()
    data = {"id": color.id, "name": color.value}
    return redirect(url_for("color.color"))


@color_blueprint.route('/api/edit', methods=['POST'])
def edit_district():
    data = request.get_json()
    id = data.get("id", None)
    value = data.get("value", None)
    if value is None or id is None:
        return jsonify({"sucess": False, "data": None})
    color = Color.query.filter(Color.id == id).first()
    color.value = value
    db.session.commit()
    data = {"id": color.id, "value": color.value}
    return jsonify({"sucess": True, "data": data})


@color_blueprint.route("/create")
def create():
    return render_template("CRUD/color/create.html", color_active="active")
