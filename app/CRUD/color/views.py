from flask import Blueprint, render_template, current_app, request, jsonify, redirect, url_for, flash
from database import access_factory
from unidecode import unidecode

color_blueprint = Blueprint(
    'color', __name__, template_folder='templates')


@color_blueprint.route('/', methods=['GET'])
def color():
    page = request.args.get("page", 1, type=int)
    res = access_factory.get_access("color").list_item(page=page)
    return render_template('CRUD/color/color.html', color_active="active", colors=res["data"], pages=res["total_pages"])


@color_blueprint.route('/api/create', methods=['POST'])
def api_create():
    data = request.values
    color_value = data.get("value", None)
    if color_value is None or color_value == "" or not access_factory.get_access("color").verify_qualified_item(value=color_value):
        flash("INPUT COLOR ERROR", "error")
        return redirect(url_for("color.color"))
    no_accent = unidecode(color_value)
    access_factory.get_access("color").create_item(value=color_value, no_accent=no_accent.lower())
    return redirect(url_for("color.color"))


@color_blueprint.route('/api/edit', methods=['POST'])
def edit_district():
    data = request.get_json()
    id = data.get("id", None)
    value = data.get("value", None)
    if value is None or id is None or not access_factory.get_access("color").verify_qualified_item(value=value):
        return jsonify({"sucess": False, "data": None})
    no_accent = unidecode(value)
    access_factory.get_access("color").edit_item(id, value=value, no_accent=no_accent.lower())
    return jsonify({"sucess": True})


@color_blueprint.route("/create")
def create():
    return render_template("CRUD/color/create.html", color_active="active")
