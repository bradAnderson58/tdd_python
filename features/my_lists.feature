Feature: My Lists
    As a logged-in usr
    I want to be able to see all my lists in one page
    So that I can find them all after I've written them

    Scenario: Create two lists and see them on the My Lists page

        Given I am a logged-in user

        When I create a list with first item "Reticulate Splines"
            And I add an item "Immanentize Eschaton"
            And I create a list with first item "Buy Milk"

        Then I will see a link to "My Lists"

        When I click the link to "My Lists"
        Then I will see a link to "Reticulate Splines"
        And I will see a link to "Buy Milk"

        When I click the link to "Reticulate Splines"
        Then I will be on the "Reticulate Splines" list page