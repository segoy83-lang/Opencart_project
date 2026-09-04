import pytest
from playwright.sync_api import sync_playwright

from pages.home_page import HomePage


@pytest.fixture
def home_page(page):
    home = HomePage(page)
    home.open()
    return home

"""@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()"""