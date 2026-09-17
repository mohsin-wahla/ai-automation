from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_proceed_to_checkout_from_shopping_cart(logged_in_page: Page):
    """
    TC-003: Proceed to checkout from the shopping cart
    """
    # Initialize Page Objects
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)

    # Precondition: The user has at least one product in the shopping cart
    products_page.add_product_to_cart("Sauce Labs Backpack")

    # Step 1: Navigate to the shopping cart page
    products_page.open_cart()

    # Step 2: Click the proceed to checkout button
    cart_page.checkout()

    # Expected Result: The user is redirected to the checkout page
    # We verify this by checking the visibility of a checkout-specific element 
    # (First Name input) defined in the CheckoutPage object.
    expect(checkout_page.first_name).to_be_visible()