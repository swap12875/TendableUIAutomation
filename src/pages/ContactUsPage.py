from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from allure import step
from src.pages.WebPage import WebPage


class ContactUsPage(WebPage):

    def __init__(self, driver, logger):
        """
        Initiates the driver object.
        :param driver:  Object of WebDriver
        :param logger:  Object of logger
        """
        super().__init__(driver, logger)
        self.wait = WebDriverWait(self.driver, 20)

    loc_mkt_cont_full_name = (By.ID, "form-input-fullName")
    loc_mkt_cont_organisation = (By.ID, "form-input-organisationName")
    loc_mkt_cont_phone_number = (By.ID, "form-input-cellPhone")
    loc_mkt_cont_email = (By.ID, "form-input-email")
    loc_mkt_cont_job_role_select = (By.ID, "form-input-jobRole")
    loc_message_field = (By.ID, "form-input-message")
    loc_mkt_cont_job_consent_agree_radio = (By.XPATH, "(//input[@type='radio'])[1]")
    loc_submit_form_error = (By.CSS_SELECTOR, "div.ff-form-errors > p")
    loc_field_validation_error = (By.CSS_SELECTOR, "ul.ff-errors > li")

    def get_contact_button_for_section(self, section):
        element_loc = (By.XPATH, f"//div[contains(.,'{section}')]/parent::div/div/button")
        return element_loc

    def get_button_with_text(self, btn_txt):
        return By.XPATH, f"//button[text()='{btn_txt}']"

    @step
    def click_contact_under_marketing(self):
        """
        click on the contact button under marketing
        """
        self.base.click_on(self.get_contact_button_for_section("Marketing"))

    @step
    def fill_up_contact_form(self, form_data, skip_fields):
        """
        fill up the form data as given
        """
        full_name, org_name, phone_num, email, job_role, msg = form_data
        self.base.send_text(self.loc_mkt_cont_full_name, full_name) if "first_name" not in skip_fields else None
        self.base.send_text(self.loc_mkt_cont_organisation, org_name) if "organisation" not in skip_fields else None
        self.base.send_text(self.loc_mkt_cont_phone_number, phone_num) if "phone_number" not in skip_fields else None
        self.base.send_text(self.loc_mkt_cont_email, email) if "email" not in skip_fields else None
        self.base.select_from_dropdown(self.loc_mkt_cont_job_role_select, job_role, "value") \
            if "job_role" not in skip_fields else None
        self.base.send_text(self.loc_message_field, msg) if "msg" not in skip_fields else None

    @step
    def message_field_text(self):
        """
        get the text from message field
        """
        return self.base.get_text(self.loc_message_field)

    @step
    def submit_the_form(self):
        """
        Click on Submit button to submit form
        """
        self.base.click_on(self.get_button_with_text('Submit'))

    @step
    def get_form_submission_error_text(self):
        """
        Get the error text for form submission.
        """
        return self.base.get_text(self.loc_submit_form_error)

    @step
    def get_field_validation_error_text(self):
        """
        Get the field validation error on form field
        """
        return self.base.get_text(self.loc_field_validation_error)

    @step
    def click_on_consent_button(self):
        """
        Click on consent button
        """
        self.base.click_on(self.loc_mkt_cont_job_consent_agree_radio)
