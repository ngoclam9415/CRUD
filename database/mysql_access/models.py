from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_fulltext import FullText, FullTextSearch
db = SQLAlchemy()

class City(FullText, db.Model):
    __tablename__ = 'city'
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent", )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    no_accent = db.Column(db.String(255), unique=True)
    district = db.relationship(
        "District", backref='city', lazy="dynamic")
    # def __init__(self, name):
    #     self.name = name

    def __repr__(self):
        return '<City %r>' % self.name


class District(FullText, db.Model):
    __tablename__ = "district"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    address = db.relationship(
        "Address", backref='district', lazy="dynamic")

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))


class Address(FullText, db.Model):
    __tablename__ = "address"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    detail = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    store = db.relationship(
        "Store", backref='address', lazy="dynamic")


class Color(FullText, db.Model):
    __tablename__ = "color"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(50), unique=True)
    no_accent = db.Column(db.String(50), unique=True)
    product_variant = db.relationship(
        "ProductVariant", backref='color', lazy="dynamic")


class Brand(FullText, db.Model):
    __tablename__ = "brand"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    category = db.relationship(
        "Category", backref='brand', lazy="dynamic")


class Category(FullText, db.Model):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    product = db.relationship(
        "Product", backref='category', lazy="dynamic")


class Store(FullText, db.Model):
    __tablename__ = "store"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    store_name = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    product_variant = db.relationship(
        "ProductVariant", backref='store', lazy="dynamic")


class Product(FullText, db.Model):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = ("no_accent",)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    no_accent = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    product_variant = db.relationship(
        "ProductVariant", backref='product', lazy="dynamic")


class ProductVariant(db.Model):
    __tablename__ = "variant"
    __table_args__ = {'extend_existing': True}
    __fulltext_columns__ = None

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.BigInteger)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))

if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_searchable import search
    from flask import Flask
    from app import create_app
    app =create_app("default")
    result = City.query.filter(FullTextSearch('Ho', City))
    print(result)