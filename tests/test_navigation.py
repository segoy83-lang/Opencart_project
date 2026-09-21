import pytest
from config import BASE_URL
from pages.home_page import HomePage
from pages.category_page import CategoryPage


@pytest.mark.parametrize(
    "menu_name, expected_route, expected_heading",
    [
        ("Настільні комп'ютери", "/desktops", "Настільні комп'ютери"),
        ("Нетбуки та Ноутбуки", "/laptop-notebook", "Нетбуки та Ноутбуки"),
    ],
)
def test_main_category_navigation(page, menu_name, expected_route, expected_heading):
    home = HomePage(page)
    home.open()
    home.open_category(menu_name)

    category = CategoryPage(page)

    assert category.heading.inner_text().strip() == expected_heading
    assert expected_route in page.url
    breadcrumb_text = category.breadcrumb.inner_text()
    home_crumb_href = category.breadcrumb.locator("a").first.get_attribute("href")
    assert "common/home" in home_crumb_href
    assert expected_heading in breadcrumb_text
    assert category.products.count() > 0

def test_header_links_are_not_broken(page):
    home = HomePage(page)
    home.open()
    home.open_account_menu()

    for link in [home.register_link, home.login_link, home.wishlist_link, home.cart_link]:
        href = link.get_attribute("href")
        assert href
        assert href != "#" and not href.startswith("javascript:")


@pytest.mark.parametrize(
    "link_name, expected_route, expected_title_fragment, needs_dropdown",
    [
        ("register_link", "account/register", "Зареєструватися", True),
        ("login_link", "account/login", "Авторизація", True),
        ("wishlist_link", "account/login", "Авторизація", False),  # logged out -> redirect
        ("cart_link", "checkout/cart", "Кошик", False),
    ],
)

def test_header_link_destinations(page, link_name, expected_route, expected_title_fragment, needs_dropdown):
    home = HomePage(page)
    home.open()


    if needs_dropdown:
        home.open_account_menu()

    link = getattr(home, link_name)
    link.click()

    assert expected_route in page.url
    assert expected_title_fragment in page.title()

    page.go_back()
    assert page.url.rstrip("/") == BASE_URL.rstrip("/")

def test_subcategory_journey_and_breadcrumb_walkback(page):
    home = HomePage(page)
    home.open()
    home.open_category("Настільні комп'ютери")

    parent = CategoryPage(page)
    parent_heading = parent.heading.inner_text().strip()

    parent.open_subcategory("Mac")

    sub = CategoryPage(page)
    sub_heading = sub.heading.inner_text().strip()
    breadcrumb_text = sub.breadcrumb.inner_text()

    home_crumb_href = sub.breadcrumb.locator("a").first.get_attribute("href")

    assert "common/home" in home_crumb_href
    assert parent_heading in breadcrumb_text
    assert sub_heading in breadcrumb_text
    assert breadcrumb_text.index(parent_heading) < breadcrumb_text.index(sub_heading)

    sub.click_breadcrumb(parent_heading)

    restored = CategoryPage(page)
    assert restored.heading.inner_text().strip() == parent_heading
    assert "/desktops" in page.url
    assert sub_heading not in restored.breadcrumb.inner_text()
