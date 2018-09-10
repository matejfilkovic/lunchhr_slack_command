from threading import Thread
import requests

from . import utils

NOT_ORDERED_MEAL_NAME = "You haven't ordered for this day."

def format_order(order):
    meal_name = order.meal_name or NOT_ORDERED_MEAL_NAME

    return f'{order.date_description} {meal_name}'

def fetch_orders(lunchhr_proxy, user_id, response_url):
    orders = lunchhr_proxy.fetch_orders(user_id)

    orders_formated = "\n".join([format_order(order) for order in orders])
    message = utils.create_slack_message(orders_formated)

    requests.post(response_url, json=message)

FETCHING_ORDERS_MESSAGE = 'Fetching your orders.'

# pylint: disable=W0613
def handle_overview(lunchhr_proxy, tokens, user_id, response_url):
    '''
    Handles overview sub command.
    '''

    Thread(
        target=fetch_orders,
        args=[lunchhr_proxy, user_id, response_url]
    ).start()

    return FETCHING_ORDERS_MESSAGE
