from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


def test_successfully_add_single_product_to_cart(logged_in_page: Page):
    """
    TC-001: Successfully add a single product to the cart as a logged-in user
    """
    # Initialize Page Objects
    products_page = ProductsPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    
    product_name = "Sauce Labs Backpack"

    # Step: Navigate to the product page or product list
    # Handled by logged_in_page fixture which logs in and redirects to the products inventory

    # Step: Select a product and click the add to cart button
    products_page.add_product_to_cart(product_name)

    # Step: Observe the cart badge
    # Expected Result: The cart badge displays '1'
    expect(
        products_page.get_cart_badge(), 
        "The cart badge should display '1' after adding one item"
    ).to_have_text("1")

    # Step: Open the shopping cart
    products_page.open_cart()

    # Expected Result: The product is successfully added to the cart 
    # and is visible within the shopping cart
    cart_item = cart_page.get_product(product_name)
    expect(
        cart_item, 
        f"The product '{product_name}' should be visible in the cart"
    ).to_be_visible()