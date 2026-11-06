"""Selenium step definitions for browser button interactions."""

from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    """Find a visible button by its text and click it."""
    driver = context.browser
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[normalize-space(.)={_xpath_literal(button_text)}]")
        )
    )
    button.click()


def _xpath_literal(value):
    """Quote text safely for an XPath string expression."""
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    parts = value.split('"')
    return "concat(" + ", '\"\', ".join(f'"{part}"' for part in parts) + ")"


@then('I should see the text "{expected_text}"')
def step_verify_text_present(context, expected_text):
    """Wait until the specified text is visible on the page."""
    driver = context.browser
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), expected_text)
    )
    assert expected_text in driver.find_element(By.TAG_NAME, "body").text, (
        f"Expected text not found: {expected_text}"
    )
