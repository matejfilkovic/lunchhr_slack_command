# pylint: disable=R0903

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

class User:
    login_page_url = 'https://www.lunch.hr'

    def __init__(self, driver, user_credentials):
        self.driver = driver
        self.is_authenticated = False
        self.user_credentials = user_credentials

    def authenticate(self):
        driver = self.driver

        driver.get(User.login_page_url)

        # Locate and click login element.
        login_element = driver.find_element_by_class_name('btn-show-login')
        login_element.click()

        # Locate credentials input elements.
        email_element = driver.find_element_by_name('email')
        password_element = driver.find_element_by_name('password')

        # Enter login credentials.
        email_element.send_keys(self.user_credentials['email'])
        password_element.send_keys(self.user_credentials['password'])

        # Submit the login form.
        login_button = driver.find_element_by_class_name('btn-login')
        login_button.click()

        wait = WebDriverWait(driver, 5)
        wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'remodal-overlay')))

        self.is_authenticated = True
