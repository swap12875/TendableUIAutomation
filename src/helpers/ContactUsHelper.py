from src.pages.ContactUsPage import ContactUsPage
from allure import step

class ContactUsHelper(ContactUsPage):
    driver = None
    logger = None
    integration_page = None

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.driver = driver
        self.logger = logger

    @step
    def submit_marketing_contact_form(self, form_data, skip_field):
        """
        Perform the form fill up for Marketing contact option
        :param form_data: data to input while filling the form
        :param skip_field: field to be skipped.
        """
        self.click_contact_under_marketing()
        self.fill_up_contact_form(form_data, skip_field)
        self.click_on_consent_button()
        self.submit_the_form()

    @step
    def verify_message_field_empty(self):
        """
        verify the message field is empty
        """
        msg_text = self.message_field_text()
        assert msg_text == "", f"message field is not empty, found: {msg_text}"

    @step
    def accept_consent(self):
        """
        accept the consent by clicking on consent radio
        """
        self.click_on_consent_button()

    @step
    def verify_error_on_form_submission(self, exp_err_txt):
        form_submit_error = self.get_form_submission_error_text()
        assert exp_err_txt in form_submit_error, (f"Unable to verify the form submission error text({exp_err_txt} "
                                                  f"with actual error text({form_submit_error}")

    @step
    def verify_field_level_error(self, field_error):
        """
        verify the error for field level validation
        :param field_error: expected error for field level validation.
        """
        form_field_error = self.get_field_validation_error_text()
        assert field_error in form_field_error, (
            f"Unable to verify the field level validation error text({field_error} "
            f"with actual error text({form_field_error}")
