import re
import sys
import time
from unittest import TestCase

from src.helpers.base import Base


class WebPage(TestCase):

    def __init__(self, driver, logger):
        """
        Initiates the driver object
        :param driver:  Instance of WebDriver
        :param logger:  Instance of logger
        """
        super().__init__("runTest")
        self.driver = driver
        self.logger = logger
        self.base = Base(self.driver, self.logger)

    from sys import platform
    root_dir_re = re.compile(r'^(.*?)src' if "win" in platform else r'^(.*?)/src')
    for paths in sys.path:
        if re.findall(root_dir_re, paths):
            ROOT_DIR = re.search(root_dir_re, paths).group(1)

    def get_page_title(self):
        page_title = self.driver.title
        self.logger.info(f"Title of the page is displayed as \n{page_title}")
        return page_title

    def get_url(self):
        time.sleep(2)
        page_url = self.driver.current_url
        self.logger.info(f"Current page url is {page_url}")
        return page_url
