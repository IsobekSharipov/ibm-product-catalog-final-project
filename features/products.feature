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
