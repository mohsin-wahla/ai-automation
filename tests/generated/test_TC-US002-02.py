from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage


def test_cart_badge_updates_correctly_when_adding_multiple_products(
    logged_in_page: Page
):
    """
    TC-US002-02: Verify cart badge updates correctly when adding multiple products
    """
    products_page = ProductsPage(logged_in_page)

    # Test Data
    products_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light"
    ]

    # Add multiple products to the cart
    for product_name in products_to_add:
        products_page.add_product_to_cart(product_name)

    # Observe and verify the cart badge
    cart_badge = products_page.get_cart_badge()
    
    # Expected result: The cart badge displays the total number of products (2)
    expect(cart_badge).to_have_text(str(len(products_to_add)))