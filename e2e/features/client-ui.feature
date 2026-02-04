Feature: Client UI
  As a user
  I want to access the client interface
  So that I can interact with the Meeting Plunger application

  Scenario: Access client home page
    Given I open the client application at "http://localhost:3000"
    Then the page title should contain "Meeting Plunger"
    And the page should display "Meeting Plunger"
    And the page should display "Local client interface"
