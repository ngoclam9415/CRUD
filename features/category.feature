Feature: Check website

#  Scenario: Open website
#    Given I open category
#    Then I print the category html

  Scenario: Open website and add new category
    Given I open category
    Then I print the category html
    Then I click add new category
    Then I add new category into form