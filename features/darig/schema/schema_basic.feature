# features/example.feature
Feature: Basic Darig Schema Validation
  As a developer
  I want to validate YAML schemas
  So that I can ensure data integrity

  Scenario: Validating a simple Darig schema by specifying model name
    Given a Darig schema "features/darig/schema/data/person.yasl" is provided
    And a YAML document "features/darig/schema/data/person.yaml" is provided
    And the model name "person" is provided
    When I run the Darig CLI with provided arguments
    Then the validation should pass

Scenario: Validating a simple Darig schema without specifying model name
    Given a Darig schema "features/darig/schema/data/person.yasl" is provided
    And a YAML document "features/darig/schema/data/person.yaml" is provided
    When I run the Darig CLI with provided arguments
    Then the validation should pass

  Scenario: Validating a directory of Darig files
    Given a Darig schema "features/darig/schema/data/dir_test" is provided
    And a YAML document "features/darig/schema/data/dir_test" is provided
    When I run the Darig CLI with provided arguments
    Then the validation should pass

  Scenario: Validating a bad directory of Darig files
    Given a Darig schema "features/darig/schema/data/bad_dir_test" is provided
    And a YAML document "features/darig/schema/data/bad_dir_test" is provided
    When I run the Darig CLI with provided arguments
    Then the validation should fail