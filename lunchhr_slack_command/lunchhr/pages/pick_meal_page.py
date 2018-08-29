# pylint: disable=C0301

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from . import config
from .base_page import BasePage

class PickMealPage(BasePage):
    def __init__(self, driver, user, order_overview_page):
        BasePage.__init__(self, driver, user)
        self.order_overview_page = order_overview_page

    def get_meal_list_for_selected_day(self, selected_day):
        self.navigate_to_selected_day(selected_day)

        return self.extract_available_meals()

    def navigate_to_selected_day(self, selected_day):
        self.order_overview_page.navigate_to_overview()
        day_picker_elements = self.order_overview_page.get_day_picker_elements()

        # Select day picker for a selected day and click it.
        selected_day_picker_elem = day_picker_elements[selected_day]
        selected_day_picker_elem.click()

        wait = WebDriverWait(self.driver, config.DEFAULT_WAITING_TIME)
        menu_button_element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'JELOVNIK')))
        menu_button_element.click()

    def extract_available_meals(self):
        meal_picker_elements = self.get_meal_picker_elements()
        meals = [self.extract_meal_name(meal_picker_element) for meal_picker_element
                 in meal_picker_elements]

        return meals

    def get_meal_picker_elements(self):
        elements = self.driver.find_elements_by_xpath("//div[contains(@class, 'DailyLunchesNavigationLink-module__container')]")

        return elements

    def extract_meal_name(self, meal_picker_elem):
        # Make a meal active by clicking a day picker elem.
        meal_picker_elem.click()

        wait = WebDriverWait(self.driver, config.DEFAULT_WAITING_TIME)
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//section[contains(@class, 'translate-top-down-enter-active')]")))

        meal_name_element = self.driver.find_element_by_xpath("//section[contains(@class, 'DailyLunchInfo-module__container')]//h1")

        return meal_name_element.text
