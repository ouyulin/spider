# !/usr/bin/env python
# -*- coding:utf-8 -*-

from core import *
from log import *
from sqlmanager import*
from threadpool import*
import sys
import os

import argparse
import unittest

if __name__ == '__main__':

    start = time.time()

    #解析参数

    ag = argparse.ArgumentParser()
    ag.add_argument('-u', '--url',
                    help='deny valid url')
    ag.add_argument('-d', '--deep', type=int, default=1,
                    help='deep must 0 < deep < 3')
    ag.add_argument('-f', '--logfile', default='/tmp/spider.log',
                    help='log file path')
    ag.add_argument('-l', '--loglevel', type=int, choices=range(1, 6),
                    default=5, help='log level in [1,5]')
    ag.add_argument('--thread', type=int, default=10,
                    help=' thread nums')
    ag.add_argument('--dbfile',
                    help='target database file')
    ag.add_argument('--key',
                    help='filter key for page content')
    ag.add_argument('--testself', action='store_true',
                    help='program self test')

    args = ag.parse_args(sys.argv[1:])
    logfile = args.logfile    # 日志文件
    loglevel = args.loglevel  # 日志等级
    dbfile = args.dbfile      # 数据库文件
    url = args.url            # 入口链接
    deep = args.deep          # 网页深度
    thread_num = args.thread  # 线程数量
    key = args.key            # 查找的关键字

    if args.testself:
        SPIDER_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.dirname(SPIDER_DIR)
        TESTS_DIR = os.path.join(ROOT_DIR, 'tests')
        TESTS_DIR = os.path.join(ROOT_DIR)
        #print TESTS_DIR
        #print sys.path
        if not TESTS_DIR in sys.path:
            sys.path.append(TESTS_DIR)
        #from test_spider import *
        from tests import test_spider
        suite = unittest.TestLoader().loadTestsFromModule(test_spider)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        print "spider start at %s" % time.strftime('%Y-%m-%d %H:%M:%S')

        #Class
        out_queue = Queue.Queue()                      # 输出队列
        work_queue = Queue.Queue()                     # 工作队列
        log_hdr = Logger(logfile, loglevel).get_hdr()  # 获取日志句柄
        sm = SQLManager(dbfile, out_queue, log_hdr)     # 打开数据库，并指定输出队列
        work_manager = Threadpool(url, deep, thread_num,
                                  log_hdr, key, work_queue, out_queue)  # 线程池
        work_manager.wait_allcomplete()

    end = time.time()
    print "cost all time: %s" % (end-start)
