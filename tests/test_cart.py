from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage


def test_product_is_visible_in_cart(
    logged_in_page: Page
):

    products_page = ProductsPage(
        logged_in_page
    )

    cart_page = CartPage(
        logged_in_page
    )

    products_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    products_page.open_cart()

    product = cart_page.get_product(
        "Sauce Labs Backpack"
    )

    expect(product).to_be_visible()
