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
    When I search for a product by name "Wireless Mouse"
    And I clear the product search form
    And I retrieve the product by its ID
    Then the response status code should be 200
    And the product name should be "Wireless Mouse"
    And the product description should be "Wireless mouse"
    And the product availability should be true
    And the product category should be "Electronics"
    And the product price should be 25.99

  Scenario: Update an existing product
    When I search for a product by name "Wireless Mouse"
    Then I should find a product named "Wireless Mouse"
    When I copy the product ID
    And I change the product name to "Gaming Mouse"
    And I press the "Update" button
    Then I should see the message "Success"
    When I clear the product search form
    And I retrieve the product using the copied ID
    Then I should find a product named "Gaming Mouse"
    When I search for a product by name "Gaming Mouse"
    Then I should find a product named "Gaming Mouse"
    When I search for a product by name "Wireless Mouse"
    Then I should not find a product named "Wireless Mouse"

  Scenario: Delete an existing product
    When I search for a product by name "Wireless Mouse"
    Then I should find a product named "Wireless Mouse"
    When I copy the product ID
    And I delete the product using the copied ID
    Then I should see the message "Product has been deleted"
    When I clear the product search form
    And I search for a product by name "Wireless Mouse"
    Then I should not find a product named "Wireless Mouse"

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
