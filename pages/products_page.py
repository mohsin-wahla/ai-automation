from playwright.sync_api import Page


class ProductsPage:

    def __init__(self, page: Page):

        self.page = page

        self.products_title = page.get_by_text("Products")

        self.cart_link = page.locator(
            '[data-test="shopping-cart-link"]'
        )

    def add_product_to_cart(self, product_name: str):

        product = self.page.locator(
            ".inventory_item"
        ).filter(
            has_text=product_name
        )

        product.get_by_role(
            "button",
            name="Add to cart"
        ).click()

    def open_cart(self):

        self.cart_link.click()

    def get_cart_badge(self):

        return self.page.locator(
            '[data-test="shopping-cart-badge"]'
        )
