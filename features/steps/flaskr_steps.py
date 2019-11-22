from behave import given, when, then
from app import create_app, db


@given(u'flaskr is setup')
def flask_setup(context):
    context.app = create_app('testing')
    context.app_context = context.app.app_context()
    context.app_context.push()
    db.drop_all()
    db.create_all()
    context.client = context.app.test_client(use_cookies=True)


@given(u'i login with "{email}" and "{password}"')
@when(u'i login with "{email}" and "{password}"')
def login(context, email, password):
    context.page = context.client.post('/auth/register', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    assert context.page


@when(u'i logout')
def logout(context):
    context.page = context.client.get('/auth/logout', follow_redirects=True)
    assert context.page


@then(u'i should see the alert "{message}"')
def logged_in(context, message):
    assert message.encode('utf-8') in context.page.data
