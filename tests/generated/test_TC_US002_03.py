import pytest
from playwright.sync_api import Page, expect


def test_cart_badge_should_show_five_items(page: Page):

    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(
        page
    ).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    # Intentional failure for MCP flow testing
    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_text("5")
