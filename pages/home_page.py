from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = ""                      # home is the site root

    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("input[name='search']")
        self.cart_badge = page.locator("#cart-total")
        self.featured_cards = page.locator("#content .product-thumb")
        self.success_alert = page.locator(".alert-success")

    def open(self):
        super().open(self.PATH)

    def card(self, index):
        return self.featured_cards.nth(index)

    def card_name(self, index):
        return self.card(index).locator("h4 a").inner_text().strip()

    def card_price(self, index):
        return self.card(index).locator(".price").inner_text().strip()


    def card_link(self, index):
        return self.card(index).locator("h4 a")

    def add_to_cart_button(self, index):
        return self.card(index).get_by_role("button", name="В кошик")

    def add_to_cart(self, index):
        before = self.cart_badge_text()
        self.add_to_cart_button(index).click()
        self.success_alert.wait_for(state="visible", timeout=5000)
        self.page.wait_for_function(
            """(before) => document.querySelector('#cart-total').innerText.trim() !== before""",
            arg=before,
            timeout=5000,
        )

    def cart_badge_text(self):
        return self.cart_badge.inner_text().strip()

    def open_cart(self):
        self.page.locator("#cart button").click()