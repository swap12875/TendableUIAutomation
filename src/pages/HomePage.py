from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from allure import step
from src.pages.WebPage import WebPage


class HomePage(WebPage):

    def __init__(self, driver, logger):
        """
        Initiates the driver object.
        :param driver:  Object of WebDriver
        :param logger:  Object of logger
        """
        super().__init__(driver, logger)
        self.wait = WebDriverWait(self.driver, 20)

    loc_top_banner = (By.CSS_SELECTOR, "#top-banner.top-banner")
    loc_top_banner_close_btn = (By.ID, "close-top-banner")
    loc_tendable_logo = (By.CLASS_NAME, "logo")
    loc_request_demo_button = (By.XPATH, "//a[.='Request A Demo']")

    @step
    def close_top_banner(self):
        """
        close the currently displayed top banner
        """
        if self.base.is_displayed(self.loc_top_banner):
            self.base.click_on(self.loc_top_banner_close_btn)

    def get_button_link_option(self, option):
        option_element = (By.XPATH, f"//div[@id='searchPanel']/parent::div[@class='button-links-panel']/"
                                    f"a[contains(.,'{option}')]")
        return option_element

    def get_top_level_menu(self, menu_name):
        menu = (By.XPATH, f"//a[contains(@class,'menu-item') and text()='{menu_name}']")
        return menu

    @step
    def logo_is_displayed(self):
        """
        Verify the logo is visible on the page.
        """
        self.base.wait_until_displayed(self.loc_tendable_logo, 'Tendable logo')
        return self.base.is_displayed(self.loc_tendable_logo)

    @step
    def top_menu_is_visible(self, menu_name):
        self.base.wait_until_displayed(self.get_top_level_menu(menu_name), f'{menu_name}: Top menu')
        return self.base.is_displayed(self.loc_tendable_logo)

    @step
    def hover_on_top_menu(self, menu_name):
        self.base.hover_mouse_on(self.base.element(self.get_top_level_menu(menu_name)))

    @step
    def submenu_under_topmenu_are_visible(self, menu_name, submenu):
        element = self.base.element(self.get_top_level_menu(menu_name))
        submenu_element_list = element.find_elements(By.XPATH,
                                                     "./parent::li/ul[contains(@class,'submenu shorten')]/li/a")
        res = False
        if len(submenu) != len(submenu_element_list):
            self.logger.info(f"sub menu count for {menu_name} is not matching with sub menu on UI")
            return False
        submenu_tuple = zip(submenu, submenu_element_list)
        for item in submenu_tuple:
            self.logger.info(f"found sub menu: {element.text} for menu: {menu_name}")
            res = True if self.base.get_text(item[1]) in item[0] else False
        return res

    @step
    def top_level_menu_is_enabled(self, menu):
        """
        Verify the menu are clickable / enabled.
        :param menu: menu tobe checked for enabled/disabled status.
        """
        return self.base.is_enabled(self.get_top_level_menu(menu), should_enabled=True)

    @step
    def navigate_from_top_menu(self, menu):
        """
        click on menu as given in param
        :param menu: menu to be clicked on
        """
        self.base.click_on(self.get_top_level_menu(menu))

    @step
    def request_demo_is_displayed(self):
        """
        verify request demo button is displayed on the page
        """
        return self.base.is_displayed(self.loc_request_demo_button)

    @step
    def verify_page_url_to_contain(self, exp_string):
        """
        Verify the Home page for the visitor.
        """
        actual_url = self.get_url()
        assert exp_string.lower() in actual_url.lower(), \
            f"Given page url({actual_url}) not contains expected string({exp_string})"

    @step
    def choose_from_button_link_panel(self, option_to_click):
        """
        click on option from button link panel
        :param option_to_click: option to be clicked
        """
        self.base.click_on(self.get_button_link_option(option_to_click))
