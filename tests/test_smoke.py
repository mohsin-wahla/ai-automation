from playwright.sync_api import expect


def test_user_can_login(logged_in_page):

    expect(logged_in_page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )
