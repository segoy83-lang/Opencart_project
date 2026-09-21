import re

from config import BASE_URL
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

PRICE_RE = re.compile(r"\d[\d\s,]*\s?Грн")


def test_home_featured_cards_are_consistent(page):
    home = HomePage(page)
    home.open()

    count = home.featured_cards.count()
    assert count > 0

    for i in range(count):
        name = home.card_name(i)
        price = home.card_price(i)
        assert name
        assert PRICE_RE.search(price), f"Unexpected price format: {price!r}"
        assert home.card_link(i).get_attribute("href")
        assert home.add_to_cart_button(i).is_visible()

def test_card_opens_matching_product(page):
    home = HomePage(page)
    home.open()

    index = 0
    expected_name = home.card_name(index)
    expected_href = home.card_link(index).get_attribute("href")

    home.card_link(index).click()

    product = ProductPage(page)
    assert expected_name in product.product_name()
    assert page.url.rstrip("/") == expected_href.rstrip("/")

    page.go_back()

    assert page.url.rstrip("/") == BASE_URL.rstrip("/")
    home_after_back = HomePage(page)
    assert home_after_back.featured_cards.count() > 0

def test_home_to_cart_journey(page):
    home = HomePage(page)
    home.open()

    index = 0
    expected_name = home.card_name(index)
    before_count = home.cart_badge_text()
    home.add_to_cart(index)

    assert home.success_alert.is_visible()

    after_count = home.cart_badge_text()
    assert after_count != before_count

    cart = CartPage(page)
    cart.open()

    assert cart.contains_product(expected_name)