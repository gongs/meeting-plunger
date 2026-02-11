Feature: Racing Game
  As a player
  I want to roll a dice to move a car
  So that I can finish a 22-step track

  Scenario: Super mode uses dice value as steps
    Given I open the racing game
    When I select super mode and roll once
    Then the displayed steps should equal the displayed dice

