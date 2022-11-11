# -*- coding: utf-8 -*-

from .db_redis import RedisDatabase
from .db_sqlite import SqliteDatabase
from lib.config import load_config


class Database(object):
    def init_db(self):
        config = load_config()
        if config['db_type'] == 'redis':
            self.db = RedisDatabase(config['redis_url'])
        elif config['db_type'] == 'sqlite':
            self.db = SqliteDatabase(config['db_name'])
        else:
            raise Exception('Database type not supported.')

        return self.db
