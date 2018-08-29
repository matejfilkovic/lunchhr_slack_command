# pylint: disable=C0103

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from lunchhr_slack_command.lunchhr import pages

credentials = {'email': '', 'password': ''}

options = Options()
driver = webdriver.Firefox(firefox_options=options)
user = pages.User(driver, credentials)
orderOverviewPage = pages.OrderOverviewPage(driver, user)
pickMealPage = pages.PickMealPage(driver, user, orderOverviewPage)
print(pickMealPage.get_meal_list_for_selected_day(2))
