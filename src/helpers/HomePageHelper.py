import time
from allure import step

from src.helpers.ContactUsHelper import ContactUsHelper
from src.pages.HomePage import HomePage


class HomePageHelper(HomePage):
    driver = None
    logger = None
    login_page = None

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger

    @step
    def verify_logo_on_homepage(self):
        """
        Verify company logo is visible on home page.
        """
        assert self.logo_is_displayed(), "Logo of the Tendable is not displayed"

    @step
    def verify_page_title(self, title):
        """
        Verify the Home page for the visitor.
        """
        actual_title = self.get_page_title()
        assert title.lower() in actual_title.lower(), \
            f"Given page title({actual_title}) not contains expected string({title})"

    @step
    def verify_top_level_menu(self, menu_n_submenu_list):
        """
        :param menu_n_submenu_list: list of menu and submenu list tuple
        """
        for idx, val in enumerate(menu_n_submenu_list):
            menu_, sub_menu = val[0], val[1]
            assert self.top_menu_is_visible(menu_), f"Top menu: {menu_} is not visible to user"
            self.hover_on_top_menu(menu_)
            if len(sub_menu) > 0:
                assert self.submenu_under_topmenu_are_visible(menu_, sub_menu), \
                    f"The Submenu under top menu: {menu_} are not visible."

    @step
    def verify_enabled_state_of_top_level_menus(self, menu_n_submenu_list):
        """
        :param menu_n_submenu_list: list of menu and submenu list tuple
        """
        for idx, val in enumerate(menu_n_submenu_list):
            menu_, sub_menu = val[0], val[1]
            assert self.top_level_menu_is_enabled(menu_)

    @step
    def verify_request_demo_on_each_top_level_menu_navigation(self, menu_list):
        """
        Navigate and verify presence of request demo on each page for top level menu navigation
        """
        for idx, val in enumerate(menu_list):
            menu_, sub_menu, url_string = val[0], val[1], val[2]
            self.navigate_from_top_menu(menu_)
            time.sleep(2)
            self.verify_page_url_to_contain(url_string)
            assert self.request_demo_is_displayed(), f"Request demo not present on the {menu_} page."

    @step
    def navigate_to_contact_us_page(self):
        """
        click and navigate to contact us page
        """
        self.choose_from_button_link_panel("Contact Us")
        self.verify_page_url_to_contain("contact-us")
        return ContactUsHelper(self.driver, self.logger)
