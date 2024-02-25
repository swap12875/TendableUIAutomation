import base64
import time

import pytest
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.helpers.browser_driver import BrowserDriver


def keyword_check(kwargs):
    kc = {}
    if 'index' in kwargs:
        kc['index'] = 'elements'
    if 'index' not in kwargs:
        kc['index'] = 'element'
    return ''.join(kc.values())


class Base:

    def __init__(self, driver, logger):
        """
        Initialized Base class
        :param driver:  Object of WebDriver
        :param logger:  Object of logger
        """
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(self.driver, 15)

    @pytest.fixture(autouse=True)
    def cli(self, logger_obj):
        """
        Gets the logger
        :param logger_obj:  Object of logger
        """
        self.logger = logger_obj

    def get_page_title(self):
        """
        Get the  page title.
        :return: page_title
        """
        page_title = self.driver.title
        self.logger.info(f"Current page title is: {page_title}")
        return page_title

    def element(self, locator, n=3, flag=None):
        """
        Return the web element with locator, wait till the poll of time 'n'
        :param locator: Locator of the web element
        :param n: Poll time
        :param flag: whether to wait for visibility of the element.
        """
        if flag is None:
            flag = False if BrowserDriver.is_headless() else True
        while n > 1:
            try:
                if flag:
                    self.wait.until(ec.visibility_of_element_located(locator),
                                    message=f"Unable to locate the element with locator {locator}")
                else:
                    self.wait.until(ec.presence_of_element_located(locator),
                                    message=f"Unable to locate the element with locator {locator}")
                element = self.driver.find_element(*locator)
                self.highlight_element(element)
                return element
            except NoSuchElementException as ns:
                n -= 1
                if n == 1:
                    raise NoSuchElementException(
                        "No such element displayed on the page with locator: {0}\n "
                        "raised exception {1}".format(str(locator), ns))
            except WebDriverException as e:
                n -= 1
                if n == 1:
                    raise NoSuchElementException("Could not locate element with value: {0}{1}".format(str(locator), e))

    def elements(self, locator, n=3):
        """
        Find the web elements on the page using locators
        :param locator: The locators for the UI elements.
        :param n: Time of attempt to find element.
        """
        while n > 1:
            try:
                self.wait.until(ec.visibility_of_any_elements_located(locator))
                elements = self.driver.find_elements(*locator)
                for ele in elements:
                    self.highlight_element(ele)
                return elements
            except WebDriverException as e:
                n -= 1
                if n == 1:
                    raise NoSuchElementException("Could not locate element list with value: {0}{1}"
                                                 .format(str(locator), e))

    def send_text(self, locator: tuple, text_str: str, element_name="input_element", is_password=False):
        """
        1. Delete the **element_name** input field,
        2. type the **text_str** to it using given locator

        :param is_password: Check if input string is password, then decode it
        :param locator: locator of input field
        :param element_name: Name of the input field for logging
        :param text_str: text string to be passed to input
        """
        if is_password:
            text_str = base64.b64decode(text_str).decode('utf-8')
        self.element(locator).clear()
        self.element(locator).send_keys(text_str)
        self.logger.info(f"String '{text_str}' sent / typed in '{element_name}' input field.")

    def click_on(self, locator, **kwargs):
        """
        1. wait till element to be clickable.
        2. click element using selenium driver
        3. If failed to clicked, click using action chains.
        :param locator: locator of the element to be clicked.
        :param kwargs:
        :return:
        """
        try:
            self.wait_until_displayed(locator)
            self.wait.until(ec.element_to_be_clickable(self.element(locator)))
            return {
                'element': lambda x: (self.element(locator).click(), self.logger.info(f"Clicked on {locator}")),

                'elements': lambda x: (self.elements(locator)[kwargs['index']].click(),
                                       self.logger.info(f"Clicked on {locator} with index {[kwargs['index']]}"))
            }[keyword_check(kwargs)]('x')
        except WebDriverException:
            self.logger.info(f"Unable to click on the element {locator}, clicking with Actions chain")
            time.sleep(1)
            action = ActionChains(self.driver)
            try:
                action.click(self.element(locator)).perform()
            except Exception as e:
                self.logger.info(f"Unable to click on the element {locator}, with action chains")
                raise e

    def wait_until_displayed(self, locator, element_name="", wait_time=0):
        """
        Wait until the element is displayed on the page.

        :param locator: Locator of the web element
        :param element_name: Name of the web element
        :param wait_time: Expected wait time for the driver
        """
        if not BrowserDriver.is_headless():
            if wait_time == 0:
                self.wait.until(ec.visibility_of_element_located(locator))
            else:
                wait = WebDriverWait(self.driver, wait_time)
                wait.until(ec.visibility_of_element_located(locator))
        self.logger.info(f"Waited for <{element_name}> Element to Display for {wait_time} seconds")

    def get_text(self, locator):
        """
        Read the text of the web element
        :param locator: Locator of the web element
        :return: Text string of the web element.
        """
        if type(locator) != WebElement:
            element = self.element(locator)
        else:
            self.highlight_element(locator)
            element = locator
        if not BrowserDriver.is_headless():
            element_text = element.text.strip()
        else:
            element_text = element.get_attribute("textContent").strip()
        self.logger.info(f"Element text for {locator} is displayed as <{element_text}>")
        return element_text

    def is_displayed(self, locator, n=2):
        """
        Verify the web  element is displayed on the page
        :param locator: Locator of the web element
        :param n: time to wait for the element to displayed.
        """
        while n > 1:
            try:
                self.wait.until(ec.visibility_of_element_located(locator))
                self.logger.info(f"Element with locator {locator} displayed on page.")
                exp_element = self.element(locator)
                self.highlight_element(exp_element)
                return exp_element.is_displayed()
            except WebDriverException:
                self.logger.info("Unable to verify the element displayed.")
                return False

    def is_enabled(self, locator, should_enabled=True, n=2):
        """
        Verify the web  element is displayed on the page
        :param locator: Locator of the web element
        :param should_enabled: to check for enabled or disabled status.
        :param n: time to wait for the element to displayed.
        """
        while n > 1:
            try:
                if should_enabled:
                    self.wait.until(ec.element_to_be_clickable(locator))
                self.logger.info(f"Element with locator {locator} is enabled/clickable.")
                return self.driver.find_element(*locator).is_enabled()
            except WebDriverException:
                self.logger.info("Unable to verify the element enabled state.")
                return False

    def highlight_element(self, element):
        if BrowserDriver.is_highlighted():
            original_style = element.get_attribute('style')
            self.driver.execute_script(
                "arguments[0].setAttribute('style', 'background: yellow; border: 2px solid red;');", element)
            WebDriverWait(self.driver, 1.0).until(lambda driver: element.get_attribute('style') != original_style)
            time.sleep(0.2)
            self.driver.execute_script("arguments[0].setAttribute('style', '{}');".format(original_style), element)

    def refresh_page(self, repeat: int = 1, difference_timeout: float = 5.0):
        """
        Reload the current application.
        """
        for i in range(0, repeat):
            self.driver.refresh()
            time.sleep(difference_timeout)
            self.logger.info(f"Current browser refreshed after {difference_timeout * (i + 1)} seconds.")

    def select_from_dropdown(self, loc_select, value, select_by="value"):
        """
        Select the option from drop down
        :param loc_select: locator of select dropdown
        :param value: value/index/text to be used for selection
        :param select_by: select by criteria
        """
        try:
            if type(loc_select) != WebElement:
                loc_select = self.element(loc_select)
            self.highlight_element(loc_select)
            select_option = Select(loc_select)
            if select_by == 'value':
                select_option.select_by_value(value)
            elif select_by == 'index':
                select_option.select_by_index(value)
            elif select_by == 'text':
                select_option.select_by_visible_text(value)
        except Exception as e:
            self.logger.error(f"Fail to select the {value}, from locator {loc_select} with exception {e}")
            pytest.fail(f"failing the test due to exception {e}")

    def hover_mouse_on(self, locator, is_element=False):
        """
        perform mouse hover action on given element
        :param locator: locator of element to hover mouse
        :param is_element: Web element to hover mouse.
        :return: if mouse is hover successfully.
        """
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(locator if not is_element else self.element(*locator)).pause(1.0).perform()
            return True
        except Exception:
            self.logger.warn(f"hover action on element {is_element} failed")
            return False
