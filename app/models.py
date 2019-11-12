from app import db


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<City %r>' % self.name
