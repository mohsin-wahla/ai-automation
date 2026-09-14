from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


def test_user_can_add_single_product_to_shopping_cart(logged_in_page: Page):
    """
    TC-US002-01: Verify that a logged-in user can add a single product to the shopping cart
    """
    # Initialize Page Objects
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    
    # Test Data
    product_name = "Sauce Labs Backpack"
    expected_badge_count = "1"

    # Step 1: Click the 'Add to Cart' button for Sauce Labs Backpack
    products_page.add_product_to_cart(product_name)

    # Step 2: Observe the cart badge count (Expected Result: displays '1')
    badge = products_page.get_cart_badge()
    expect(badge).to_have_text(expected_badge_count)

    # Step 3: Navigate to the shopping cart page
    products_page.open_cart()

    # Step 4: Verify Sauce Labs Backpack is visible in the shopping cart
    cart_item = cart_page.get_product(product_name)
    expect(cart_item).to_be_visible()