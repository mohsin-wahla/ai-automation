from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_complete_purchase(
    logged_in_page: Page
):

    products_page = ProductsPage(
        logged_in_page
    )

    cart_page = CartPage(
        logged_in_page
    )

    checkout_page = CheckoutPage(
        logged_in_page
    )

    # Add product
    products_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    # Open cart
    products_page.open_cart()

    # Verify product
    product = cart_page.get_product(
        "Sauce Labs Backpack"
    )

    expect(product).to_be_visible()

    # Checkout
    cart_page.checkout()

    # Customer information
    checkout_page.enter_customer_information(
        "Ali",
        "Khan",
        "60000"
    )

    checkout_page.continue_checkout()

    # Finish
    checkout_page.finish_order()

    # Verify order
    expect(
        logged_in_page.get_by_text(
            "Thank you for your order!"
        )
    ).to_be_visible()
