from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_proceed_to_checkout_from_cart(logged_in_page: Page):
    """
    TC-US002-03: Verify ability to proceed to checkout from the cart
    """
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    
    product_name = "Sauce Labs Backpack"

    # Precondition: A product has been added to the shopping cart
    products_page.add_product_to_cart(product_name)

    # Step 1: Navigate to the shopping cart page
    products_page.open_cart()

    # Step 2: Click the 'Checkout' button
    cart_page.checkout()

    # Expected Result: The user is successfully redirected to the checkout flow
    # Validation: Check if an element unique to the checkout information page is visible
    expect(checkout_page.first_name).to_be_visible()