import logging
import logging.handlers
import os
import sys


if sys.argv[0] and os.path.splitext(sys.argv[0])[1] == ".py":
    s = os.path.split(sys.argv[0])
    logger = logging.getLogger(s[1])
else:
    logger = logging.getLogger('WF')

logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if os.path.exists('/var/run/syslog'):
    shandler = logging.handlers.SysLogHandler('/var/run/syslog')
elif os.path.exists('/dev/log'):
    shandler = logging.handlers.SysLogHandler('/dev/log')
else:
    shandler = logging.handlers.SysLogHandler()
shandler.setFormatter(formatter)
logger.addHandler(shandler)


chandler = logging.StreamHandler()
chandler.setFormatter(formatter)
logger.addHandler(chandler)

def SetLevel(level):
    global logger
    logger.setLevel(level)


