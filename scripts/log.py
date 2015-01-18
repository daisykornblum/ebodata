# -*- coding: utf-8 -*-
import time

logfile = '/home/daisy/ebola/scripts/everything.log'

def log(msg, filename=None):
    if filename is None:
        filename = logfile

    stamp = time.strftime('[%Y-%m-%d %H:%M:%S]')

    with open(filename, "a") as log:
        log.write("%s %s" % (stamp, msg))