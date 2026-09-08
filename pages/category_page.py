from pages.base_page import BasePage


class CategoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("#content h2")
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.products = page.locator(".product-thumb")

    def open_subcategory(self, name):
        self.page.get_by_role("link", name=name, exact=False).first.click()


    def click_breadcrumb(self, name):
        self.breadcrumb.get_by_role("link", name=name).click()



