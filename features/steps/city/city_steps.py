from behave import given, when, then
from app import create_app, db


@given(u'When get into "city" page with blank list and click the button with id "create-btn".')
def step_impl_1(context):
    print("HERE" + context.url + "/city")
    context.browser.get(context.url + "/city")
    
    
    create_button = context.browser.find_element_by_css_selector(".btn.btn-lg.btn-accent.ml-auto")
    print(create_button)
    create_button.click()


@when(u'When redirected to create window, at "cityName" form, i type in "Ho Chi Minh" and click on button with css ".btn.btn-primary"')
def step_impl_2(context):
    city_form = context.browser.find_element_by_name("cityName")
    city_form.send_keys("Ho Chi Minh")
    create_button= context.browser.find_element_by_css_selector(".mb-2.btn.btn-primary.mr-2.w-100")
    create_button.click()

@then(u'When redirected back to list window, i should see "Ho Chi Minh"')
def step_impl_3(context):
    last_button = context.browser.find_element_by_css_selector(".page-item.last.disabled")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    ciy_field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert ciy_field_text ==  "Ho Chi Minh"