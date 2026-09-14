from ai.failure_analyzer import FailureAnalyzer


def main():

    analyzer = FailureAnalyzer()

    analysis = analyzer.analyze(
        test_name="test_logged_in_user_can_add_single_product_to_cart",

        error_message="""
AssertionError: Locator expected to have text '1'
but received '0'
""",

        test_code="""
def test_logged_in_user_can_add_single_product_to_cart(logged_in_page):

    products_page = ProductsPage(logged_in_page)

    products_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )

    expect(
        products_page.get_cart_badge()
    ).to_have_text("1")
"""
    )

    print("\n===== AI FAILURE ANALYSIS =====\n")
    print(analysis)


if __name__ == "__main__":
    main()
