import random
import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_key():
    salt = hashlib.sha1(str(random.random())).hexdigest()[:10]
    return hashlib.sha1(salt).hexdigest()


class Pages(object):

    def __init__(self):
        self.__registry = dict()

    def __getitem__(self, name):
        return self.__registry[name]

    def __setitem__(self, name, value):
        self.__registry[name] = value

    def __iter__(self):
        return iter(sorted(self.__registry.keys()))


PAGES = Pages()


def add_account_page(url):
    def decorator(f):
        PAGES[url] = f
        return f
    return decorator
