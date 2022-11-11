# -*- coding: utf-8 -*-

import logging
import os
import yaml


def create_logger() -> logging.Logger:
    config = load_config()
    _logger = logging.getLogger(config['log_name'])
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(config['log_file'])
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    return _logger


def load_config():
    """
    Load config from conf/config.yaml
    {'db_type': 'sqlite',
     'db_name': 'sqlite:///db/stacker.db',
     'redis_url': 'redis://localhost:6379/0',
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
        'db_type': os.getenv('DB_TYPE', _config.get('db_type')),
        'db_name': os.environ.get('DB_NAME', _config.get('db_name', 'sqlite:///db/stacker.db')),
        'redis_url': os.environ.get('REDIS_URL', _config.get('redis_url')),
        'log_name': os.environ.get('LOG_NAME', _config.get('log_name', 'StackerNews')),
        'log_file': os.environ.get('LOG_FILE', _config.get('log_file', 'log/stacker-news-top.log')),
        'tg_chat_id': os.environ.get('TG_CHAT_ID', _config.get('tg_chat_id')),
        'tg_token': os.environ.get('TG_TOKEN', _config.get('tg_token'))
    }

    if _config_env['db_type'] not in ['sqlite', 'redis']:
        raise Exception('Invalid database type.')
    if not _config_env['tg_chat_id'] or not _config_env['tg_token']:
        raise ValueError('Missing Telegram chat_id or token.')

    return _config_env

