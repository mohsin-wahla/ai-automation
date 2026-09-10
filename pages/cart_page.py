from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):

        self.page = page

        self.checkout_button = page.get_by_role(
            "button",
            name="Checkout"
        )

    def get_product(self, product_name: str):

        return self.page.locator(
            ".cart_item"
        ).filter(
            has_text=product_name
        )

    def checkout(self):

        self.checkout_button.click()
