Feature: Health Check
  As a system administrator
  I want to verify that all services are running
  So that I can ensure the system is operational

  Scenario: Backend health check
    Given the backend service is running on "http://localhost:8000"
    When I request the health endpoint
    Then the response status should be 200
    And the response should contain "healthy"

  Scenario: Client health check
    Given the client service is running on "http://localhost:3000"
    When I request the health endpoint
    Then the response status should be 200
    And the response should contain "healthy"
