import collections

from .pages.user import User

UserPages = collections.namedtuple('UserPages',
                                   ['order_overview_page',
                                    'pick_meal_page',
                                    'order_page'])

def authenticate_and_create_pages(selenium_driver, user_credentials):
    user = User(selenium_driver, user_credentials)
    user.authenticate()

    return user
