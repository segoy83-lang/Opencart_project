from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("h1")
        self.add_to_cart_button = page.locator("#button-cart")
        self.success_alert = page.locator(".alert-success")

    def product_name(self):
        return self.heading.inner_text().strip()

    def add_to_cart(self):
        self.add_to_cart_button.click()