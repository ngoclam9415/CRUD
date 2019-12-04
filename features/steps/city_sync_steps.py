from behave import given, when, then
from unidecode import unidecode
import time

def send_delayed_keys(element, text, delay=0.1) :
    for c in text :
        # endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(delay)

@given(u'Open {content_type} page')
def open_city_page(context, content_type):
    print("HERE" + context.url + "/{}".format(content_type))
    context.browser.get(context.url + "/{}".format(content_type))

@when(u'Create a new {city}')
def create_new_city(context, city):
    create_button= context.browser.find_element_by_css_selector(".btn.btn-lg.btn-accent.ml-auto")
    create_button.click()
    city_input = context.browser.find_element_by_name("cityName")
    city_input.send_keys(city)
    create_button= context.browser.find_element_by_css_selector(".mb-2.btn.btn-primary.mr-2.w-100")
    create_button.click()

@then(u'Check if {city} is listed')
def check_listed_city(context, city):
    last_button = context.browser.find_element_by_css_selector(".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    ciy_field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert ciy_field_text == city

@then(u'Check if {city} existed in mongo')
def check_existed_city_in_mongo(context, city):
    data = {"no_accent" : unidecode(city).lower()}
    existed = not context.mongo_db.select("City").verify_qualified_item(**data)
    assert existed == True

@given(u'Previous create step')
def do_nothing(context):
    pass

@when(u'Search with {keyword}')
def input_search_city(context, keyword):
    search_input = context.browser.find_element_by_id("search")
    send_delayed_keys(search_input, keyword)
    # search_input.send_keys(keyword)
    search_button = context.browser.find_element_by_css_selector(".btn.btn-outline-success.my-2.my-sm-0")
    search_button.click()

@then(u'Check if {city} listed in search results')
def check_existed_city_in_search(context, city):
    bodyText = context.browser.find_element_by_tag_name("body")
    assert city in bodyText.text

@when(u'Edit {city} with {new_city}')
def edit_city(context, city, new_city):
    context.browser.find_element_by_xpath('//*[@id="body-city"]/tr[contains(., "{}")]/td[3]'.format(city)).click()
    city_name = context.browser.find_element_by_name('city_name')
    city_name.clear()
    send_delayed_keys(city_name, new_city)
    context.browser.find_element_by_id('modify').click()


@then(u'Check if {city} is listed in current page')
def check_listed_modify_city(context, city):
    bodyText = context.browser.find_element_by_tag_name("body")
    assert city in bodyText.text