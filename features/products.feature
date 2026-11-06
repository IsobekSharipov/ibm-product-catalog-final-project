Feature: Product Catalog Management
  As a user of the Product Catalog API
  I want to retrieve product information
  So that I can view product details

  Background:
    Given the following products exist
      | id | name           | category    | description    | price | available |
      | 1  | Wireless Mouse | Electronics | Wireless mouse | 25.99 | true      |
      | 2  | Keyboard       | Electronics | USB keyboard   | 49.99 | true      |

  Scenario: Read an existing product
    When I request the product with ID 1
    Then the response status code should be 200
    And the product name should be "Wireless Mouse"
    And the product category should be "Electronics"
    And the product price should be 25.99

  Scenario: Update an existing product
    When I update the product with ID 1 with name "Gaming Mouse" and price 39.99
    Then the response status code should be 200
    And the product name should be "Gaming Mouse"
    And the product price should be 39.99
    When I request the product with ID 1
    Then the response status code should be 200
    And the product name should be "Gaming Mouse"
    And the product price should be 39.99

  Scenario: Delete an existing product
    When I delete the product with ID 2
    Then the response status code should be 204
    When I request the product with ID 2
    Then the response status code should be 404

  Scenario: List all products
    When I request the list of all products
    Then the response status code should be 200
    And the response should contain 2 products
    And the product list should contain "Wireless Mouse"
    And the product list should contain "Keyboard"

  Scenario: Search products by category
    When I search for products in category "Electronics"
    Then the response status code should be 200
    And the response should contain 2 products
    And the product list should contain "Wireless Mouse"
    And the product list should contain "Keyboard"
    And all returned products should belong to category "Electronics"

  Scenario: Search products by availability
    When I search for products with availability "true"
    Then the response status code should be 200
    And the response should contain 2 products
    And the product list should contain "Wireless Mouse"
    And the product list should contain "Keyboard"
    And all returned products should have availability "true"

  Scenario: Search products by name
    When I search for products with name "Wireless Mouse"
    Then the response status code should be 200
    And the response should contain 1 products
    And the product list should contain "Wireless Mouse"
    And all returned products should have name "Wireless Mouse"
