from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "index.php?route=checkout/cart"

    def __init__(self, page):
        super().__init__(page)
        self.page_title = page.locator("h1")
        self.line_items = page.locator("#content table tbody tr")

    def open(self):
        super().open(self.PATH)

    def contains_product(self, product_name):
        return self.line_items.filter(has_text=product_name).count() > 0