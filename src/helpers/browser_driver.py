import os
import re
import sys
import time
import unittest
from io import BytesIO

import pytest
from PIL import Image
from dotenv import load_dotenv
from pytest_html_reporter import attach
from allure import attach as allure_attach
from selenium.common import WebDriverException


class BrowserDriver(unittest.TestCase):
    """
    Initialize the Driver for browser methods associated with Test execution
    """

    web_browser = None
    driver = None
    implicit_wait_time = None
    user_agent = None
    from sys import platform
    root_dir_re = re.compile(r'^(.*?)src' if "win" in platform else r'^(.*?)/src')
    for paths in sys.path:
        if re.findall(root_dir_re, paths):
            ROOT_DIR = re.search(root_dir_re, paths).group(1)
    test_name = None
    skip_tests = None

    def __init__(self, test_name):
        super().__init__(test_name)
        self.test_name = test_name

    def read_env_file(self):
        """
        Reads the .env file contents
        """
        global headless_mode
        global element_highlight
        load_dotenv(self.ROOT_DIR + '/.env')
        self.web_browser = os.getenv('BROWSER')
        self.user_agent = os.getenv('USER_AGENT')
        self.is_highlight = os.getenv('IS_ELEMENT_HIGHLIGHT')
        self.form_data_source = os.getenv('TEST_DATA_SOURCE')
        self.implicit_wait_time = float(os.getenv('IMPLICITLY_WAIT'))
        self.url = os.getenv('URL')
        self.skip_tests = os.getenv('SKIP_TEST')
        headless_mode = True if 'headless' in self.web_browser else False
        element_highlight = True if ('True' in self.is_highlight and not headless_mode) else False

    def setUp(self):
        """
        Prepare env for Test execution.
        """
        if self.test_name != "runTest":
            self.logger.info("Starting Test {0}".format(self.test_name))
        self.read_env_file()
        if self.test_name in self.skip_tests:
            pytest.skip("Skipping the test -> " + self.test_name)

    def tearDown(self):
        exc_err_info = self._outcome.result._excinfo
        if exc_err_info is None:
            self.logger.info(f"_____________ Test Case: {self.test_name} passed _____________")
        else:
            self.logger.fatal(f'~~~~~~~~~~~~~~~~~~ Test Case: {self.test_name} Failed ~~~~~~~~~~~~~~~~~~~~~with >'
                              f"\n\t\t\t\t\t\t {exc_err_info[0].typename}: {exc_err_info[0].value}")
            time.sleep(1)
            failed_snap = self.get_failed_tc_screenshot_path()
            failed_tc_file = failed_snap + str(self.test_name) + '.png'
            total_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.set_window_size(self.driver.get_window_size()['width'], height=total_height)
            screenshot = self.driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))
            image.save(failed_tc_file)
            self.logger.info(f"Failed TC {self.test_name} screenshot saved as: \n\t\t\t\t\t\t {failed_tc_file}")
            attach(data=failed_tc_file)
            allure_attach(failed_tc_file)
        # attach(data=self.driver.get_screenshot_as_png())
        self.close_exe_driver()
        if self.test_name != "runTest":
            self.logger.info("Test Execution Finished for TC: {0}".format(self.test_name))

    def get_failed_tc_screenshot_path(self):
        file_sep = os.sep
        failed_snap = os.path.join(self.ROOT_DIR + f"report{file_sep}failed_tc{file_sep}")
        return failed_snap

    @pytest.fixture(autouse=True)
    def cli(self, logger_obj):
        """
        Initializes the variables passed from CLI
        :param logger_obj:  Logger Object
        """
        self.logger = logger_obj

    @pytest.fixture(scope="session", autouse=True)
    def close_driver_and_server(self):
        """
        Close driver after execution.
        """
        yield self.driver
        if self.driver is not None:
            try:
                self.driver.quit()
                self.logger.info("Driver Closed.")
            except WebDriverException:
                pass
        else:
            self.logger.info("Driver is already closed.")

    def browser_navigation(self, logger=None):
        """
        Initialize web driver for test execution.
        :param logger: Logger instance
        :return: driver
        """
        from selenium import webdriver
        options = None

        if logger is not None:
            self.logger = logger
        if self.web_browser in 'chrome-headless':
            options = webdriver.ChromeOptions()
            options.add_argument('disable-infobars')
            if BrowserDriver.is_headless():
                options.add_argument('--headless')
                # options.add_argument(
                #     f"user-agent=User-Agent: {self.user_agent}")
            options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                }
            })
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.driver = webdriver.Chrome(options=options)
        elif self.web_browser in 'edge-headless':
            options = webdriver.EdgeOptions()
            if self.is_headless():
                options.add_argument('--headless')
            self.driver = webdriver.Edge(options=options)
        elif self.web_browser in 'firefox-headless' or self.web_browser in 'ff-headless':
            options = webdriver.FirefoxOptions()
            if self.is_headless():
                options.add_argument('--headless')
            self.driver = webdriver.Firefox(options=options)
        else:
            pytest.fail("Invalid value for driver provided in .env file.")
        self.driver.maximize_window()
        self.driver.implicitly_wait(self.implicit_wait_time)
        # actions = ActionChains(self.driver)
        # self.driver.current_url()
        # actions.w3c_actions
        self.driver.get(self.url)
        self.logger.info(f"Initializing driver {self.web_browser} with Headless mode {self.is_headless()}")
        return self.driver

    def close_exe_driver(self):
        """
        Close current driver for chrome.
        """
        try:
            if self.driver is not None:
                self.driver.quit()
                self.logger.info("Chrome browser closed successfully.\n\n\n")
        except Exception:
            self.logger.info("Chrome browser is already closed.\n\n\n")

    @pytest.fixture(autouse=True)
    def get_user_cred(self, get_test_data):
        """
        Reads Test Data from the test_data py file
        :param get_test_data:   Object of test_data
        """
        self.data = get_test_data
        self.app_data = self.data.get('app_data')
        self.form_data = self.data.get('form_data')
        self.error_text = self.data.get('error_text')

    @staticmethod
    def is_headless():
        return headless_mode

    @staticmethod
    def is_highlighted():
        return element_highlight


if __name__ == '__main__':
    unittest.main()
