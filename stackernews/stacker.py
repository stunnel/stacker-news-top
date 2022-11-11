# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lib import Database, session, logger, replace, telegram_bot_send_text


class StackerNews(object):
    def __init__(self):
        self.domain = 'https://stacker.news'
        self.url = f'{self.domain}/top/posts?when=day'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                        'Referer': self.domain
                        }
        self.message_template = '*{title}*\n_{sats} sats, {comments} comments_\n{url}'  # Markdown format
        self.session = session
        self.db = Database()

        self.soup_top = None        # BeautifulSoup object
        self.threads = []           # BeautifulSoup objects of threads
        self.threads_list = []      # List of threads, dicts with keys: id, title, sats, comments
        self.threads_send = []      # List of threads to be sent, dicts with keys: id, title, sats, comments

        self.class_threads = 'item_hunk__I7noX'
        self.class_thread = 'item_title__f5MGn text-reset mr-2'
        self.class_sats = 'item_other__qNlji'
        self.class_comments = 'text-reset'

    def get_top(self):
        """
        Get top page of Stacker News and save it to self.soup_top
        """
        logger.info('Getting html from: {}'.format(self.url))
        try:
            response = self.session.get(self.url, headers=self.headers, timeout=60)
            response.encoding = 'utf-8'
            self.soup_top = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            logger.error(e)

    def get_threads(self):
        """
        Get threads from top page of Stacker News and save them to self.threads
        """
        logger.info('Getting threads.')
        self.threads = self.soup_top.find_all('div', class_=self.class_threads)
        logger.info('Got {} threads.'.format(len(self.threads)))

    def get_thread(self):
        """
        Decode thread from BeautifulSoup object and save it to self.threads_list
        """
        for thread in self.threads:
            thread_url = thread.find('a', class_=self.class_thread).get('href')
            # /items/59757
            thread_id = int(thread_url.split('/')[-1])
            thread_title = thread.find('a', class_=self.class_thread).text
            thread_sats = thread.find('div', class_=self.class_sats).find('span').text.replace(' sats', '')
            thread_comments = thread.find_all('a', class_=self.class_comments)[1].text.replace(' comments', '')
            thread = {'id': thread_id, 'title': thread_title, 'sats': thread_sats, 'comments': thread_comments}
            self.threads_list.append(thread)
        logger.info('Decode {} threads.'.format(len(self.threads_list)))

    def check_sent(self):
        """
        Check if thread is already sent and if not, if not, add it to self.threads_send
        """
        for thread in self.threads_list:
            thread_db = self.db.get_thread(thread['id'])
            if thread_db:
                logger.info('Thread "{}" exist in db, skip sending.'.format(thread['id']))
                continue
            logger.info('Thread "{}" not exist in db, will be sent.'.format(thread['id']))
            self.threads_send.append(thread)

    def send_threads(self):
        """
        Send threads from self.threads_send to telegram
        """
        logger.info('There are {} threads to be sent.'.format(len(self.threads_send)))
        for thread in self.threads_send:
            logger.info('Sending thread "{}".'.format(thread['id']))
            logger.info('Adding thread "{}" to db.'.format(thread['id']))
            self.db.add_thread(thread['id'], thread['title'], thread['sats'], thread['comments'])
            url = '{domain}/items/{thread}'.format(domain=self.domain, thread=thread['id'])
            message = self.message_template.format(title=replace(thread['title']),
                                                   sats=thread['sats'],
                                                   comments=thread['comments'],
                                                   url=replace(url))
            logger.info('Message "{}" will be sent.'.format(message))
            result = telegram_bot_send_text(message)
            logger.info('Sending result: {}'.format(result))

    def init(self):
        self.threads = []
        self.threads_list = []
        self.threads_send = []

    def run(self):
        self.init()
        self.get_top()
        self.get_threads()
        self.get_thread()
        self.check_sent()
        self.send_threads()
