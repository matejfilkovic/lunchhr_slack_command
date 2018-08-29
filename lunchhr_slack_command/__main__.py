# pylint: disable=C0103

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .lunchhr.pages import User

credentials = {'email': '', 'password': ''}

options = Options()
driver = webdriver.Firefox(firefox_options=options)
user = User(driver, credentials)
user.authenticate()
