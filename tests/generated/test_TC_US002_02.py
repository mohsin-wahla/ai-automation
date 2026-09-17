import pytest
from playwright.sync_api import Page, expect


def test_added_product_is_visible_in_cart(page: Page):

    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(
        page
    ).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    page.locator('[data-test="shopping-cart-link"]').click()

    expect(
        page.locator('[data-test="inventory-item-name"]')
    ).to_have_text("Sauce Labs Backpack")
