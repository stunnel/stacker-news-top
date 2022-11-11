# -*- coding: utf-8 -*-

from lib.utils import session
from lib.config import load_config


class TelegramBot(object):
    def __init__(self):
        self.config = load_config()
        self.url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.config['tg_token'])

    def send(self, message):
        data = {'chat_id': self.config['tg_chat_id'],
                'text': message,
                'parse_mode': 'MarkdownV2'}
        response = session.post(self.url, json=data, headers={'Accept': 'application/json'})
        return response.json()
