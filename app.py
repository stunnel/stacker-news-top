#!/usr/bin/python3
# -*- coding: utf-8 -*-

import schedule
from stackernews import StackerNews

stacker = StackerNews()
schedule.every(10).minutes.do(stacker.run)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
