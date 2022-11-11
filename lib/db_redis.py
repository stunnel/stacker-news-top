# -*- coding: utf-8 -*-

import redis


class RedisDatabase(object):
    def __init__(self, redis_url):
        self.r = redis.Redis.from_url(redis_url)

    def add_thread(self, thread_id: int, title: str, sats: int, comments: int):
        """
        Add a thread to the database.
        :param thread_id: The thread id to add.
        :param title: The thread title to add.
        :param sats: The thread sats to add.
        :param comments: The thread comments to add.
        """
        self.r.hmset(thread_id, {'title': title, 'sats': sats, 'comments': comments})

    def get_thread(self, thread_id: int) -> dict:
        """
        Get a thread from the database.
        :param thread_id: The thread id to get.
        :return: The thread object.
        """
        return self.r.hgetall(thread_id)

    def del_thread(self, thread_id: int):
        """
        Delete a thread from the database.
        :param thread_id: The thread id to delete.
        """
        self.r.delete(thread_id)
