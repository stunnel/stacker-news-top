#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from stackernews import StackerNews

stacker = StackerNews()

scheduler = BlockingScheduler(timezone='Asia/Hong_Kong')
scheduler.add_job(stacker.run, 'interval', minutes=1, id='stacker',
                  max_instances=1, next_run_time=datetime.datetime.now())


if __name__ == '__main__':
    scheduler.start()
