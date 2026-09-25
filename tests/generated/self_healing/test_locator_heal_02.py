from playwright.sync_api import Page, expect


def test_self_heal_bike_locator(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    # INTENTIONAL LOCATOR DEFECT
    page.locator(
        '[data-test="add-to-cart-sauce-labs-bike-light"]'
    ).click(timeout=5000)

    expect(
        page.locator('[data-test="shopping-cart-badge"]')
    ).to_have_text("1")