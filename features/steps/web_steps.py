"""Selenium step definitions for browser button interactions."""

from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@when('I press the "{button_text}" button')
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


@then('I should not see the text "{unexpected_text}"')
def step_verify_text_absent(context, unexpected_text):
    """Wait until the specified text is absent from visible page content."""
    driver = context.browser
    WebDriverWait(driver, 10).until_not(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), unexpected_text)
    )
    visible_text = driver.find_element(By.TAG_NAME, "body").text
    assert unexpected_text not in visible_text, (
        f"Unexpected text is still visible: {unexpected_text}"
    )


@then('I should see the message "{expected_message}"')
def step_verify_message_present(context, expected_message):
    """Wait for an expected message to appear in visible page text."""
    driver = context.browser
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), expected_message)
    )
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert expected_message in page_text, (
        f"Expected message was not displayed: {expected_message}"
    )


@then('I should see "{expected_text}" in the results')
def step_verify_text_in_results(context, expected_text):
    """Wait for the expected text inside the search results element."""
    driver = context.browser
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), expected_text)
    )
    results = driver.find_element(By.ID, "search_results")
    assert expected_text in results.text, (
        f"Expected text not found in search results: {expected_text}"
    )
