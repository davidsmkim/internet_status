from src.constants import WWW_PREFIX


def create_url(host: str, domain_ending: str) -> str:
    """
    Takes in a host (ex: google) and a domain ending (ex: com) and returns a
    full url (ex: www.google.com)
    """
    return WWW_PREFIX + host + domain_ending
