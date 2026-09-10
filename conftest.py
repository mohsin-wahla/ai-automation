import pytest

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page):

    login_page = LoginPage(page)

    login_page.open()

    login_page.login(
        "standard_user",
        "secret_sauce"
    )

    return page
