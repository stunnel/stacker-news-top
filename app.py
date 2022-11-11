#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from stackernews import StackerNews

stacker = StackerNews()

scheduler = BackgroundScheduler(timezone='Asia/Hong_Kong')
scheduler.add_job(stacker.run, 'interval', minutes=10, id='stacker', next_run_time=datetime.datetime.now())


if __name__ == '__main__':
    scheduler.start()
