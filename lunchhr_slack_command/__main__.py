from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from .lunchhr.pages import User

credentials = { 'email': '', 'password': '' }

options = Options()
driver = webdriver.Firefox(firefox_options=options)
user = User(driver, credentials)
user.authenticate()