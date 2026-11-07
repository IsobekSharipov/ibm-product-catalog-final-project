Feature: Product Catalog Management
  As a user of the Product Catalog API
  I want to retrieve product information
  So that I can view product details

  Background:
    Given the following products exist
      | id | name           | category    | description    | price | available |
      | 1  | Wireless Mouse | Electronics | Wireless mouse | 25.99 | true      |
      | 2  | Keyboard       | Electronics | USB keyboard   | 49.99 | true      |
      | 3  | Office Chair   | Furniture   | Desk chair    | 89.99 | true      |
      | 4  | Gaming Monitor | Electronics | LED monitor   | 199.99 | false     |

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
    Given I am on the "Home Page"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Wireless Mouse" in the results
    And I should see "Keyboard" in the results

  Scenario: Search products by category
    Given I am on the "Home Page"
    When I press the "Clear" button
    And I select "Electronics" in the "category" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Wireless Mouse" in the results
    And I should see "Keyboard" in the results
    And I should not see "Office Chair" in the results

  Scenario: Search products by availability
    Given I am on the "Home Page"
    When I press the "Clear" button
    And I select "True" in the "available" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Wireless Mouse" in the results
    And I should see "Keyboard" in the results
    And I should not see "Gaming Monitor" in the results

  Scenario: Search products by name
    Given I am on the "Home Page"
    When I press the "Clear" button
    And I enter "Wireless Mouse" in the "name" field
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Wireless Mouse" in the results
    And I should see "Wireless mouse" in the results
