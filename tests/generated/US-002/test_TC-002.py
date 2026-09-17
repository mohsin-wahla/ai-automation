from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage


def test_cart_badge_increments_when_multiple_products_added(logged_in_page: Page):
    """
    TC-002: Verify cart badge increments when multiple products are added
    """
    products_page = ProductsPage(logged_in_page)

    # Add the first product to the cart
    products_page.add_product_to_cart("Sauce Labs Backpack")

    # Observe the cart badge displays '1'
    cart_badge = products_page.get_cart_badge()
    expect(cart_badge).to_have_text("1")

    # Add a second product to the cart
    products_page.add_product_to_cart("Sauce Labs Bike Light")

    # Observe the cart badge displays '2'
    expect(cart_badge).to_have_text("2")