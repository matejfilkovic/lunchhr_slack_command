import collections

from .pages.user import User
from .pages.order_overview_page import OrderOverviewPage
from .pages.pick_meal_page import PickMealPage
from .pages.order_page import OrderPage

UserPages = collections.namedtuple('UserPages',
                                   ['order_overview_page',
                                    'pick_meal_page',
                                    'order_page'])

def authenticate_and_create_pages(selenium_driver, user_credentials):
    user = User(selenium_driver, user_credentials)
    user.authenticate()

    order_overview_page = OrderOverviewPage(selenium_driver, user)
    pick_meal_page = PickMealPage(selenium_driver, user, order_overview_page)
    order_page = OrderPage(selenium_driver, user, pick_meal_page)

    return UserPages(order_overview_page, pick_meal_page, order_page)
