import logging
import os
import re
import sys

import pytest

from Test_Data.test_data import test_data

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def logger_obj():
    """
    Initiate the logger instance for execution.
    :return: instance of the logger.
    """
    report_folder_path = get_report_folder_path()
    # Check whether path exists or not
    is_exist = os.path.exists(report_folder_path)
    if not is_exist:
        os.makedirs(report_folder_path)

    log_file_path = report_folder_path + get_file_seperator_for_os() + "execution.log"
    ch = logging.FileHandler(log_file_path, mode='w', encoding="utf-8")
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', '%m/%d/%Y %I:%M:%S %p')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_report_folder_path():
    from sys import platform
    logger.setLevel(logging.DEBUG)
    root_dir_re = re.compile(r'^(.*?)src' if "win" in platform else r'^(.*?)/src')
    for paths in sys.path:
        if re.findall(root_dir_re, paths):
            root_dir = re.search(root_dir_re, paths).group(1)
    return root_dir + "report"


def get_file_seperator_for_os():
    file_separator = os.sep
    return file_separator


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Make report after completion of execution.
    :param item: Testcase
    """

    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    """
    Failed test operation.
    Check if a test has failed
    """
    yield
    if request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            pytest.start_new_session = True
            logger.info(f'~~~~~~~~~~~~~~~~~~~~~~~~~ Test Case : {request.node.name} Failed ~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                        .upper())
        else:
            logger.info(f"_____________ Test Case : {request.node.name} passed _____________")


@pytest.fixture(scope="session", autouse=True)
def clean_up_screenshot_folder():
    """
    Clean up and Create 'failed_tc' dir
    """
    # cleaning up 'failed_tc' directory
    failed_tc_dir = os.path.join(get_report_folder_path() +
                                 get_file_seperator_for_os() + "failed_tc" + get_file_seperator_for_os())
    is_exist = os.path.exists(failed_tc_dir)
    if not is_exist:
        # Create a new directory (failed_tc) if it does not exist
        os.makedirs(failed_tc_dir)
    for filename in os.scandir(failed_tc_dir):
        os.remove(os.path.join(failed_tc_dir, filename))
        logger.info(f'existing screenshot files under {failed_tc_dir} deleted successfully.')
    yield


@pytest.fixture
def get_test_data():
    """
    Get the test data for execution.
    """
    return test_data
