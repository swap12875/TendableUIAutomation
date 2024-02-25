from src.helpers.browser_driver import BrowserDriver
from src.helpers.HomePageHelper import HomePageHelper


class TestTendableHomeModule(BrowserDriver):
    homepage_helper: HomePageHelper = None

    def __init__(self, test_name):
        super().__init__(test_name)

    def test_TCID_001_verify_homepage(self):
        """
        verify valid home page UI
        """
        self.driver = self.browser_navigation()
        self.homepage_helper = HomePageHelper(self.driver, self.logger)
        self.homepage_helper.close_top_banner()
        self.homepage_helper.verify_logo_on_homepage()
        self.homepage_helper.verify_page_title(self.app_data["home_page_title"])

    def test_TCID_002_verify_top_level_menus(self):
        """
        Requirement: Confirm accessibility of the top-level menus:
        Home, Our Story, Our Solution, and Why Tendable.
        """
        self.driver = self.browser_navigation()
        self.homepage_helper = HomePageHelper(self.driver, self.logger)
        self.homepage_helper.close_top_banner()
        self.homepage_helper.verify_enabled_state_of_top_level_menus(self.app_data["top_level_menus"])
        self.homepage_helper.verify_top_level_menu(self.app_data["top_level_menus"])

    def test_TCID_003_verify_request_demo_option_on_menu_pages(self):
        """
        Requirement: verify the 'Request demo option present on each page'
        """
        self.driver = self.browser_navigation()
        self.homepage_helper = HomePageHelper(self.driver, self.logger)
        self.homepage_helper.close_top_banner()
        self.homepage_helper.verify_request_demo_on_each_top_level_menu_navigation(self.app_data["top_level_menus"])
