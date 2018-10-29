import time

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
        menu_button_element = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, 'JELOVNIK'))
        )
        menu_button_element.click()

    def extract_available_meals(self):
        meal_picker_elements = self.get_meal_picker_elements()
        meals = [
            self.extract_meal_details(meal_picker_element)
            for meal_picker_element in meal_picker_elements
        ]

        return meals

    def get_meal_picker_elements(self):
        meal_picker_element_xpath = (
            "//div[contains(@class, "
            "'DailyLunchesNavigationLink-module__container')]"
        )
        elements = self.driver.find_elements_by_xpath(meal_picker_element_xpath)

        return elements

    def extract_meal_details(self, meal_picker_elem):
        # Make a meal active by clicking a day picker elem.
        meal_picker_elem.click()

        # Give a browser enough time to refresh the meal
        # elements.
        time.sleep(1)

        # Wait until an animation completes.
        animation_element_xpath = (
            "//section[contains(@class, 'translate-top-down-enter-active')]"
        )
        wait = WebDriverWait(self.driver, config.DEFAULT_WAITING_TIME)
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, animation_element_xpath)
            )
        )

        meal_name_element_xpath = (
            "//section[contains(@class, "
            "'DailyLunchInfo-module__container')]//h1"
        )
        meal_name_element = self.driver.find_element_by_xpath(
            meal_name_element_xpath
        )

        background_image_element = self.driver.find_element_by_class_name(
            'l-daily-lunch-image'
        )

        background_image_url = background_image_element.value_of_css_property(
            'background-image'
        )[5:-2]

        salad_element = self.driver.find_element_by_xpath(
            ("//span[contains(@class, "
             "'DailyLunchInfo-module__subtitle')]")
        )

        calories_element = self.driver.find_element_by_xpath(
            ("//h1[contains(@class, "
             "'DailyLunchNutrientsTable-module__calorificValueContainer')]")
        )

        return {
            'name': meal_name_element.text,
            'image': background_image_url,
            'calories': calories_element.text,
            'side_dish': salad_element.text
        }
