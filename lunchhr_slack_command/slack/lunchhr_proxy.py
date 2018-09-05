from selenium import webdriver

from ..lunchhr import factory

class LunchhrProxy:
    def __init__(self, selenium_driver):
        self.selenium_driver = selenium_driver
        self.user_pages_map = {}

    def authenticate_user_and_create_pages(self, slack_user_id, credentials):
        userPages = factory.authenticate_and_create_pages(self.selenium_driver,
                                                          credentials)

        self.user_pages_map[slack_user_id] = userPages

    @staticmethod
    def create():
        selenium_driver = webdriver.Firefox()
        return LunchhrProxy(selenium_driver)