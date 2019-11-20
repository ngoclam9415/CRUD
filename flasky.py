from app import create_app
from database.mysql_access.models import db
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

try:
    with app.app_context():
        db.create_all()
except:
    pass

if __name__ == "__main__":
    app.run(debug=True)
