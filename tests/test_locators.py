import re

from pages.category_page import CategoryPage

PRICE_RE = re.compile(r"\d[\d\s,]*\s?Грн")

def test_category_all_cards_valid(page):
    category = CategoryPage(page)
    category.open()

    assert category.products.count() > 0

    for card in category.products.all():
        name_link = card.locator("h4 a")
        name = name_link.inner_text().strip()
        href = name_link.get_attribute("href")
        price = card.locator(".price").inner_text().strip()
        add_button = card.get_by_role("button", name="В кошик")

        assert name
        assert href and href != "#"
        assert PRICE_RE.search(price), f"Unexpected price format: {price!r}"
        assert add_button.is_visible()

def test_two_cards_are_independent(page):
    category = CategoryPage(page)
    category.open()

    card_a = category.products.nth(0)
    card_b = category.products.nth(1)

    name_link_a = card_a.locator("h4 a")
    name_link_b = card_b.locator("h4 a")

    name_a = name_link_a.inner_text().strip()
    href_a = name_link_a.get_attribute("href")

    name_b = name_link_b.inner_text().strip()
    href_b = name_link_b.get_attribute("href")

    assert name_a and name_b
    assert name_a != name_b
    assert href_a != href_b

    name_link_a.click()

    h1_text = page.locator("h1").inner_text().strip()
    assert h1_text.startswith(name_a) or name_a in h1_text

def test_add_selected_product_to_cart(page):
    category = CategoryPage(page)
    category.open()

    target_name = "HTC Touch HD"
    matched = category.card_by_text(target_name)

    assert matched.count() == 1  # content match is unambiguous

    card_name = matched.locator("h4 a").inner_text().strip()
    assert target_name in card_name

    before_count = category.cart_badge.inner_text().strip()

    add_button = matched.get_by_role("button", name="В кошик")
    add_button.click()

    category.success_alert.wait_for(state="visible", timeout=5000)
    assert category.success_alert.is_visible()
    assert target_name in category.success_alert.inner_text()

    page.wait_for_function(
        """(before) => document.querySelector('#cart-total').innerText.trim() !== before""",
        arg=before_count,
        timeout=5000,
    )
    after_count = category.cart_badge.inner_text().strip()
    assert after_count != before_count