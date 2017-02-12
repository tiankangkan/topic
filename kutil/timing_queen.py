# -*- coding: UTF-8 -*-

"""
Desc: the queen has a timer.
Note:

---------------------------------------
# 2016/08/25   kangtian         created

"""
import Queue
import time
import traceback
import threading
import random


class TimingQueen(object):
    """
    Notes:
        full_handler or timeout_handler need set_oldest_time !!
    """
    SIGNAL_TIMEOUT = "SIGNAL_TIMEOUT"
    SIGNAL_FULL = "SIGNAL_FULL"
    SIGNAL_OK = "SIGNAL_OK"

    def __init__(self, max_size, timeout=None, async_handle=True):
        self.queen_size = max_size
        self.queen = Queue.Queue(max_size)
        self.oldest_time = time.time()
        self.timeout = timeout or 10
        self.timeout_handler = None
        self.full_handler = None
        self.async_handle = async_handle

    def set_oldest_time(self, oldest_time=None):
        self.oldest_time = oldest_time or time.time()

    def set_timeout_handler(self, function, args=None, kwargs=None, callback=None):
        self.timeout_handler = dict(function=function, args=args, kwargs=kwargs, callback=callback)

    def set_full_handler(self, function, args=None, kwargs=None, callback=None):
        self.full_handler = dict(function=function, args=args, kwargs=kwargs, callback=callback)

    def apply_handler(self, handler):
        h = handler
        function, args, kwargs, callback = h.get('function'), h.get('args', []), h.get('kwargs', {}), h.get("callback", None)
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs
        try:
            if callback:
                func = lambda: callback(function(timing_queen=self, *args, **kwargs))
            else:
                func = lambda: function(timing_queen=self, *args, **kwargs)
            if self.async_handle:
                threading.Thread(target=func).start()
            else:
                func()
            self.set_oldest_time()
        except Exception as ex:
            self.set_oldest_time()
            if callback:
                callback(ex)
            else:
                print traceback.format_exc()

    def put(self, item):
        if self.queen.full():
            if self.full_handler:
                self.apply_handler(self.full_handler)
        now = time.time()
        if self.queen.qsize() == 0:
            self.oldest_time = now
        # print 'timer_queen: put: now: %s, oldest_time: %s' % (now, self.oldest_time)
        if now - self.oldest_time > self.timeout:
            if not self.timeout_handler:
                return self.SIGNAL_TIMEOUT
            else:
                # print "timer_queen: hit timeout"
                self.apply_handler(self.timeout_handler)
        self.queen.put(item)
        if self.queen.full():
            return self.SIGNAL_FULL

        return self.SIGNAL_OK


if __name__ == "__main__":
    pass
