from behave import *


@given('I open category')
def step_impl(context):
    context.browser.get(context.url + "/category")


@then('I print the category html')
def step_impl(context):
    title = context.browser.find_element_by_tag_name('h3')
    assert "Category Table" in title.text\

@then('I click add new category')
def step_impl(context):
    context.browser.find_element_by_css_selector('.btn.btn-lg.btn-accent.ml-auto').click()

@then('I add new category into form')
def step_impl(context):
    category_name = context.browser.find_element_by_name('category_name')
    category_name.send_keys('Do an vat so 1 viet nam')
    brand_id = context.browser.find_element_by_name('brand_id')
    brand_id.send_keys('1')
    context.browser.find_element_by_css_selector('.mb-2.btn.btn-primary.mr-2.w-100').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "Category Table" in title.text