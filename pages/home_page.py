from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = ""                      # home is the site root

    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("input[name='search']")

    def open(self):
        super().open(self.PATH)