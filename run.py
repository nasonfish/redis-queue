from queue import Queue

config = {
    "tasks": 2,
    "interval": 10,  # seconds between running each task
    "redis-port": 6379,
    "redis-hostname": "localhost"
}

print(
    """
    Staring queue manager. We will now read from the redis database
    for any objects that need to be run from here.
    We will be using the redis server %s:%s, executing %s task(s) every %s second(s).
    Edit the configuration in run.py to change that.
    """ % (config['redis-hostname'], config['redis-port'], config['tasks'], config['interval'])
)

Queue(config).start()
