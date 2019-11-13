from app import db, create_app



class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    district = db.relationship(
        "District", backref='city', lazy="dynamic")

    # def __init__(self, name):
    #     self.name = name

    def __repr__(self):
        return '<City %r>' % self.name


class District(db.Model):
    __tablename__ = "district"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    address = db.relationship(
        "Address", backref='district', lazy="dynamic")

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))


class Address(db.Model):
    __tablename__ = "address"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    detail = db.Column(db.String(50))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
