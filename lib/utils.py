# -*- coding: utf-8 -*-

import yaml
import logging
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


def create_logger(logger_name: str, log_file: str) -> logging.Logger:
    _logger = logging.getLogger(logger_name)
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    return _logger


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


def load_config():
    """
    Load config from conf/config.yaml
    """
    with open('../conf/config.yaml', 'r') as f:
        _config = yaml.safe_load(f)
        return _config


config = load_config()
session = create_session()
logger = create_logger(config['log_name'], config['log_file'])
