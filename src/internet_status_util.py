import datetime
import random
from typing import Tuple

from src.constants import WWW_PREFIX


def create_url(host: str, domain_ending: str) -> str:
    """
    Takes in a host (ex: google) and a domain ending (ex: com) and returns a
    full url (ex: www.google.com)
    """
    return WWW_PREFIX + host + domain_ending


def get_datetime() -> str:
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime('%x')
    current_time = current_datetime.strftime('%X')
    return current_date + '@' + current_time


def get_random_host(hosts: Tuple) -> str:
    return random.choice(hosts)
