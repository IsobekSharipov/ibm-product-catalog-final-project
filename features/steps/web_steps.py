"""Selenium step definitions for browser button interactions."""

from behave import when
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
