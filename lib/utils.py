# -*- coding: utf-8 -*-

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning

replace_map = {'_': '\\_',
               '*': '\\*',
               '[': '\\[',
               ']': '\\]',
               '(': '\\(',
               ')': '\\)',
               '~': '\\~',
               '`': '\\`',
               '>': '\\>',
               '#': '\\#',
               '+': '\\+',
               '-': '\\-',
               '=': '\\=',
               '|': '\\|',
               '{': '\\{',
               '}': '\\}',
               '.': '\\.',
               '!': '\\!'
               }


def create_session(connections=20, retries=5, backoff_factor=2,
                   status_forcelist=None, disable_warnings=False) -> requests.Session:
    _session = requests.Session()
    if disable_warnings is True:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        urllib3.disable_warnings()
    status_forcelist = status_forcelist or (429, 500, 502, 503, 504)
    retry = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapters = HTTPAdapter(pool_connections=connections, max_retries=retry)
    _session.mount('https://', adapters)
    return _session


def replace(string: str) -> str:
    """
    Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of
    replacement mappings. For example, if I supplied
    the string "Hello world.", and the mappings
    {"H": "J", ".": "!"}, it would return "Jello world!".

    ref: https://core.telegram.org/bots/api#formatting-options

    :param string: string to replace characters in.
    """
    for character, replacement in replace_map.items():
        string = string.replace(character, replacement)
    return string


def string_to_int(string: str) -> int:
    def is_digit(string: str) -> bool:
        string = string.replace('.', '', 1)
        return string.isdigit()

    def remove_dot(string) -> str:
        return string.replace('.', '', 1)

    string = string.strip().lower().replace(',', '')
    try:
        result = int(float(string))
    except ValueError:
        if string.endswith('k') and is_digit(string[:-1]):
            result = int(float(string[:-1]) * 1000)
        elif string.endswith('m') and is_digit(string[:-1]):
            result = int(float(string[:-1]) * 1000000)
        elif string.endswith('b') and is_digit(string[:-1]):
            result = int(float(string[:-1]) * 1000000000)
        else:
            result = 0

    return result


session = create_session()
