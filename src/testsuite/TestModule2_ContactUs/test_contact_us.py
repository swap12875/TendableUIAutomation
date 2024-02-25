import time

from src.helpers.ContactUsHelper import ContactUsHelper
from src.helpers.HomePageHelper import HomePageHelper
from src.helpers.browser_driver import BrowserDriver
from Utils.TestDataGenerator import form_data


class TestContactUsModule(BrowserDriver):
    homepage_helper: HomePageHelper = None
    contactus_helper: ContactUsHelper = None

    def __init__(self, test_name):
        super().__init__(test_name)

    def test_TCID_004_fill_up_form_on_contact_us_page_with_static_data(self):
        """
        fill up contact us form with static test data
        """
        self.driver = self.browser_navigation()
        self.homepage_helper = HomePageHelper(self.driver, self.logger)

        self.contactus_helper = self.homepage_helper.navigate_to_contact_us_page()
        self.contactus_helper.submit_marketing_contact_form(
            (self.form_data["first_name"],
             self.form_data["organization_name"],
             self.form_data["phone_number"],
             self.form_data["email"],
             self.form_data["job_role"],
             self.form_data["msg"]),
            skip_field=["msg"]
        )
        self.contactus_helper.verify_message_field_empty()
        self.contactus_helper.verify_error_on_form_submission(self.error_text["submit_form_error_text"])
        self.contactus_helper.verify_field_level_error(self.error_text["field_validation_error"])

    def test_TCID_004_fill_up_form_on_contact_us_page_with_random_data(self):
        """
        fill up contact us form with random test data
        """
        self.driver = self.browser_navigation()
        self.homepage_helper = HomePageHelper(self.driver, self.logger)

        self.contactus_helper = self.homepage_helper.navigate_to_contact_us_page()
        self.contactus_helper.submit_marketing_contact_form(
            (form_data["first_name"],
             form_data["organization_name"],
             form_data["phone_number"],
             form_data["email"],
             form_data["job_role"],
             ""),
            skip_field=["msg"]
        )
        self.contactus_helper.verify_error_on_form_submission(self.error_text["submit_form_error_text"])
        self.contactus_helper.verify_field_level_error(self.error_text["field_validation_error"])
        time.sleep(5)
