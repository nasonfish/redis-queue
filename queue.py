import functions
import redis
from threading import Thread
import time


class Queue:
    r = None
    config = {}

    def __init__(self, config):
        self.r = redis.StrictRedis(host=config['redis-hostname'], port=config['redis-port'], db=0)
        self.init_db()
        self.config = config

    def init_db(self):
        if not self.r.exists("queue:next"):
            self.r.set('queue:next', 0)  # queue:next is our counter for executing.
            # queue:enter is the counter for inserting

    def start(self):
        while True:
            for i in range(0, self.config['tasks']):
                Task(self.r).start()
            time.sleep(self.config['interval'])


class Task(Thread):

    r = None

    def __init__(self, r):
        Thread.__init__(self)
        self.r = r

    def run(self):
        tid = self.next()
        if tid is None:
            print("Thread ending, no tasks were found.")
            return
        tid = int(tid)
        line = self.r.pipeline()  # so we can do this all at once
        res = line.get('queue:%s:file' % tid).get('queue:%s:task' % tid).smembers('queue:%s:args' % tid).execute()
        res[2] = list(res[2])
        print('Executing ID %s - %s.%s(%s)' % (tid, res[0], res[1], ', '.join(res[2])))
        getattr(getattr(functions, res[0]), res[1])(*res[2])

    def next(self):
        lua = """
        local value = redis.call('GET', 'queue:next')
        value = tonumber(value)
        value = value + 1
        local exists = redis.call('EXISTS', 'queue:' .. value .. ":task")
        if exists == 1 then
            return tonumber(redis.call("INCR", 'queue:next'))
        end
        return nil
        """

        # tid = self.r.incr('queue:next')  # this returns the new value. we know two threads won't get the same value.
        #if not self.r.exists('queue:%s:task' % tid):
        #    self.r.decr('queue:next')
        #    return
        check = self.r.register_script(lua)
        return check()
