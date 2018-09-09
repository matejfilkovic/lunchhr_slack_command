from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from . import config
from .base_page import BasePage

class OrderPage(BasePage):
    def __init__(self, driver, user, pick_meal_page):
        BasePage.__init__(self, driver, user)
        self.pick_meal_page = pick_meal_page

    def order_meal(self, selected_day, selected_meal, selected_time):
        self.put_selected_meal_in_basket(selected_day, selected_meal)
        self.navigate_to_basket()
        self.order_for_selected_time(selected_time)

    def put_selected_meal_in_basket(self, selected_day, selected_meal):
        self.pick_meal_page.navigate_to_selected_day(selected_day)

        selected_meal_picker_element = (
            self.pick_meal_page.get_meal_picker_elements()[selected_meal]
        )

        selected_meal_picker_element.click()

        # Wait until an animation stops.
        animation_elem_xpath = (
            "//section[contains(@class, 'translate-top-down-enter-active')]"
        )

        wait = WebDriverWait(self.driver, config.DEFAULT_WAITING_TIME)
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, animation_elem_xpath)
            )
        )

        add_to_basket_elem = self.driver.find_element_by_xpath(
            "//a[contains(@class, 'LunchActionButton-module__button')]"
        )

        add_to_basket_elem.click()

    def order_for_selected_time(self, selected_time):
        # Wait until a loading element disappears.
        loading_element_xpath = (
            "//div[contains(@class, 'LoadingContainer-module__overlay')]"
        )
        wait = WebDriverWait(self.driver, config.LONGER_WAITING_TIME)
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, loading_element_xpath)
            )
        )

        time_picker_elements = self.get_time_picker_elements()

        # Select time for a delivery.
        selected_time_picker_element = time_picker_elements[selected_time]
        selected_time_picker_element.click()

        # Place an order.
        order_button = self.driver.find_element_by_xpath(
            "//a[contains(@class, 'LunchActionButton-module__button')]"
        )
        order_button.click()

        # Creation of an order can take some time so wait time needs
        # to be increased.
        wait = WebDriverWait(self.driver, config.LONGER_WAITING_TIME)
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cartSuccessModal')
            )
        )

    def get_time_picker_elements(self):
        time_pickers_xpath = (
            "//div[contains(@class, "
            "'CartPeriodSelector-module__buttonContainer')]"
        )

        elements = self.driver.find_elements_by_xpath(
            time_pickers_xpath
        )

        return elements

    def navigate_to_basket(self):
        basket_element = (
            self.driver
            .find_element_by_partial_link_text('Košarica')
        )

        basket_element.click()
