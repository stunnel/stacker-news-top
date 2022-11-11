# -*- coding: utf-8 -*-

import os
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
    {'db_name': 'sqlite:///db/stacker.db',
     'log_name': 'StackerNews',
     'log_file': 'log/stacker-news-top.log',
     'tg_chat_id': -1000000000001,
     'tg_token': '123456789:TELEGRAM_BOT_TOKEN_SAMPLE'
    }
    """
    try:
        with open('conf/config.yaml', 'r') as f:
            _config = yaml.safe_load(f)
    except FileNotFoundError:
        return load_config_from_env({})
    except yaml.YAMLError:
        return load_config_from_env({})
    except Exception:
        return load_config_from_env({})

    return load_config_from_env(_config)


def load_config_from_env(_config):
    """
    Load config from environment variables.
    """
    _config_env = {
        'db_name': os.environ.get('DB_NAME', _config.get('db_name') or 'sqlite:///db/stacker.db'),
        'log_name': os.environ.get('LOG_NAME', _config.get('log_name') or 'StackerNews'),
        'log_file': os.environ.get('LOG_FILE', _config.get('log_file') or 'log/stacker-news-top.log'),
        'tg_chat_id': os.environ.get('TG_CHAT_ID', _config.get('tg_chat_id')),
        'tg_token': os.environ.get('TG_TOKEN', _config.get('tg_token'))
    }

    if not _config_env['tg_chat_id'] or not _config_env['tg_token']:
        raise ValueError('Missing Telegram chat_id or token.')

    return _config_env

config = load_config()
session = create_session()
logger = create_logger(config['log_name'], config['log_file'])
