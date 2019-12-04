from selenium import webdriver
from flasky import app
from database.mysql_access.models import db as mysql_db
from database.mongo_access.models import db as mongo_db
from app import create_app
import threading
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
from elasticsearch import Elasticsearch


def before_all(context):
    print("Executing before all")
    context.app = create_app('default')
    context.app_context = context.app.app_context()
    context.app_context.push()
    context.mysql_db = mysql_db
    context.mongo_db = mongo_db
    context.mysql_db.drop_all()
    context.mysql_db.create_all()
    context.mongo_db.drop_all()
    context.mongo_db.create_all()
    es = Elasticsearch()
    es.indices.delete("_all")
    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(context.app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()
    print("HERE")
    context.url = "http://localhost:5000"
    context.client = context.app.test_client(use_cookies=True)
    context.browser = webdriver.Chrome('dependencies/chromedriver')
    context.browser.maximize_window()
    context.browser.implicitly_wait(20)


def before_feature(context, feature):
    context.mysql_db.drop_all()
    context.mysql_db.create_all()
    context.mongo_db.drop_all()
    context.mongo_db.create_all()
    print("Before feature\n")


# Scenario level objects are popped off context when scenario exits
def before_scenario(context, scenario):
    print("Before scenario\n")


def after_scenario(context, scenario):
    print("After scenario\n")


def after_feature(context, feature):
    print("\nAfter feature")


def after_all(context):
    print("Executing after all")
    context.browser.quit()
    context.server.shutdown()
    context.pa_app.join()
    




