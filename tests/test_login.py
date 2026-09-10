from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

def test_valid_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_invalid_login(page: Page):

    login_page = LoginPage(page)

    login_page.open()

    login_page.login(
        "standard_user",
        "wrong_password"
    )

    error_message = page.locator(
        '[data-test="error"]'
    )

    expect(error_message).to_be_visible()