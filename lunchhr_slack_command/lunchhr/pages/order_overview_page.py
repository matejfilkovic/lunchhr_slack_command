import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from . import config
from .base_page import BasePage
from .exceptions import OrderDetailsElementMissingException
from .models import Order

class OrderOverviewPage(BasePage):
    def get_orders(self):
        self.navigate_to_overview()

        return self.expand_orders()

    def navigate_to_overview(self):
        self.authenticate_if_needed()

        wait = WebDriverWait(self.driver, config.DEFAULT_WAITING_TIME)
        overview_element = wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Pregled'))
        )

        overview_element.click()

    def expand_orders(self):
        day_picker_elements = self.get_day_picker_elements()
        orders = [
            self.expand_order(day_picker_element) for day_picker_element
            in day_picker_elements
        ]

        return orders

    def get_day_picker_elements(self):
        elements = self.driver.find_elements_by_xpath(
            "//div[contains(@class, 'CalendarDay-module__container')]"
        )

        return elements

    def expand_order(self, day_picker_element):
        # Make a day active by clicking a day picker elem.
        day_picker_element.click()

        date_description = self.driver.find_element_by_xpath(
            "//div[contains(@class, 'CalendarDay-module__dateContainerActive')]"
        ).text

        meal_name = self.extract_meal_name_for_selected_day()

        return Order(date_description, meal_name)

    def extract_meal_name_for_selected_day(self):
        driver = self.driver

        # Give a browser enough time to refresh the meal
        # elements.
        time.sleep(1)

        # pylint: disable=C0301

        try:
            meal_name_element = driver.find_element_by_xpath(
                "//h1[contains(@class, 'OrderDetails-module__title')]"
            )

            return meal_name_element.text
        except NoSuchElementException:
            try:
                # If an order details element is missing, check whether an element
                # for an empty order is missing. If the empty element is missing, we
                # have a problem :/.
                driver.find_element_by_xpath(
                    "//div[contains(@class, 'UserOrdersOverview-module__emptyOrdersOverview')]"
                )
            except NoSuchElementException:
                raise OrderDetailsElementMissingException()
