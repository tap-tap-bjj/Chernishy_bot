
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def is_element_present(self, how, what):
    try:
        self.browser.find_element(how, what)
    except (NoSuchElementException, TimeoutException):
        return False
    return


def is_element_clickable(self, how, what):
    try:
        self.wait(EC.element_to_be_clickable((how, what)))
    except (NoSuchElementException, TimeoutException):
        return False
    return True
