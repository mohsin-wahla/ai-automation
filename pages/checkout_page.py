from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):

        self.page = page

        self.first_name = page.get_by_placeholder(
            "First Name"
        )

        self.last_name = page.get_by_placeholder(
            "Last Name"
        )

        self.postal_code = page.get_by_placeholder(
            "Zip/Postal Code"
        )

        self.continue_button = page.get_by_role(
            "button",
            name="Continue"
        )

        self.finish_button = page.get_by_role(
            "button",
            name="Finish"
        )

    def enter_customer_information(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ):

        self.first_name.fill(first_name)

        self.last_name.fill(last_name)

        self.postal_code.fill(postal_code)

    def continue_checkout(self):

        self.continue_button.click()

    def finish_order(self):

        self.finish_button.click()
