Feature: Test all function of /city

    Scenario: Open a blank table, then create the very first city
        Given When get into "city" page with blank list and click the button with id "create-btn".
        When When redirected to create window, at "cityName" form, i type in "Ho Chi Minh" and click on button with css ".btn.btn-primary"
        Then When redirected back to list window, i should see "Ho Chi Minh"