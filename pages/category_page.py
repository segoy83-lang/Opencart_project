from pages.base_page import BasePage


class CategoryPage(BasePage):
    PATH = "desktops"


    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("#content h2")
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.products = page.locator(".product-thumb")
        self.cart_badge = page.locator("#cart-total")
        self.success_alert = page.locator(".alert-success")

    def open(self):
        super().open(self.PATH)

    def open_subcategory(self, name):
        self.page.get_by_role("link", name=name, exact=False).first.click()

    def click_breadcrumb(self, name):
        self.breadcrumb.get_by_role("link", name=name).click()

    def card_by_text(self, text):
        return self.products.filter(has_text=text)



