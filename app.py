#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from stackernews import StackerNews

stacker = StackerNews()

scheduler = BlockingScheduler(timezone='Asia/Hong_Kong')
scheduler.add_job(stacker.run, 'interval', minutes=10, id='stacker')


if __name__ == '__main__':
    scheduler.start()
