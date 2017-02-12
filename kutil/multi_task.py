# -*- coding: UTF-8 -*-

"""
Desc: multi task util.
Note:

---------------------------------------
# 2016/08/24   kangtian         created

"""


def map_func_async(func, args_list, worker_num=None):
    from multiprocessing.dummy import Pool
    worker_num = worker_num or 8
    job = lambda args: func(*args)
    p = Pool(worker_num)
    p.map(job, args_list)


def multi_task(func, args_list, worker_num=None):
    from multiprocessing.dummy import Pool
    worker_num = worker_num or 8
    job = lambda args: func(args)
    p = Pool(worker_num)
    p.map(job, args_list)
