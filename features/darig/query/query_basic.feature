Feature: Basic Darig Query
  As a developer
  I want to query YAML data using SQL
  So that I can perform complex data analysis

  Scenario: Loading a schema and data, then executing a SQL query
    Given a Darig schema "features/darig/schema/data/person.yasl" is loaded
    And YAML data "features/darig/schema/data/person.yaml" is loaded
    When I run the Darig query "SELECT * FROM acme_person"
    Then the query should return 2 rows
    And the row should contain "John Doe"

  Scenario: Running the Darig query CLI in interactive mode
    When I run the Darig query CLI with "--interactive"
    Then the CLI should show the welcome message "Welcome to the Darig Query shell."
