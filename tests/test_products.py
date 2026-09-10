from playwright.sync_api import Page, expect

from conftest import logged_in_page
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_add_product_to_cart(logged_in_page):


    products_page = ProductsPage(logged_in_page)

    products_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    expect(
        products_page.get_cart_badge()
    ).to_have_text("1")
