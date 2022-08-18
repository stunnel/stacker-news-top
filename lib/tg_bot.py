# -*- coding: utf-8 -*-

from lib import session, config

url = 'https://api.telegram.org/bot{}/sendMessage'.format(config['tg_token'])


def telegram_bot_send_text(message):
    """
    Send message to telegram channel/chat_id/group via telegram bot.
    """
    data = {'chat_id': config['tg_chat_id'],
            'text': message,
            'parse_mode': 'MarkdownV2'}
    response = session.post(url, json=data, headers={'Accept': 'application/json'})
    return response.json()
