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
    from wsgiref import simple_server
    from wsgiref.simple_server import WSGIRequestHandler
    server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    server.set_app(app)
    server.serve_forever()
    # app.run(debug=True)

