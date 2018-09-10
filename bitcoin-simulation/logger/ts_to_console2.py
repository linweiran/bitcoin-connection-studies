from lib import *
from bitcoin import *
from bitcoin.net import *
from bitcoin.core import *
from bitcoin.messages import *
import logging

import time
import datetime
from cStringIO import StringIO
from bisect import insort, bisect
from pprint import pprint as pp
from collections import defaultdict
import struct
import json 
import socket





import argparse
import gzip
import glob
import struct
import re
import sys
import logger
sys.path.append('../')
from lib import *

def within(ts, start, delta):
    return (start <= ts <= start + delta)

def filets(filename):
    try:
        return int(re.findall('verbatim.log-\d{4}-\d{2}-\d{2}-(\d+)' , filename.split('.gz')[0])[0])
    except IndexError as e:
        return 0

def parse_record(record):
    sid, log_type, timestamp, rest = logger.log.deserialize_part(record)
    log = logger.type_to_obj[log_type].deserialize(sid, timestamp, rest)
    return sid, log_type, timestamp, log

def readfile(logfile, tofile, start, delta):
    if '.gz' in logfile:
        f = gzip.open(logfile, 'rb')
    else:
        f = open(logfile, 'rb')

#    if (tofile):
#        output = open('output.log', 'ab')
#    else:
#        output = sys.stdout
#    output.write(f.read())
#    output.close()
    seen=set()
    minute=0
    count=0
    with open("minutes-hash.csv","w") as output:
      while True:
        length = f.read(4)
        if length == '':
            return
        try:
            length, = struct.unpack('>I', length)
        except Exception as e:
            print e
            break
        record = f.read(length)
        sid, log_type, timestamp, log = parse_record(record) 

        try:
            msg = MsgSerializable.stream_deserialize(StringIO(log.bitcoin_msg))
        except:
            continue
        if int(timestamp/60000000.0) <> minute:
		minute=int(timestamp/60000000.0)
		print minute,count,datetime.datetime.fromtimestamp(minute*60).isoformat()
		output.write("{},{}\n".format(str(minute),str(count)))
		count=0

        if msg is None: continue
        if msg.command == 'inv':
            for cinv in msg.inv:
                hash=b2lx(cinv.hash)
		if hash not in seen:
			seen.add(hash)
			count+=1
   
#        if within(timestamp/1000000.0, start, delta):
#            output.write(record + '\n')

def main(logdir, start, delta, tofile):
    logfiles = sorted(glob.glob(logdir + '/verbatim.log-*'))
    targets = []
    tslast = filets(logfiles[-1])
    last = -1
    capture = False
    for logfile in logfiles:
        ts = filets(logfile)
        if last < start <= ts:
            capture = True
        if capture:
            targets.append(logfile)
        if start + delta < ts:
            capture = False
        last = ts       
    if capture:
        targets.append(logdir + '/verbatim.log')
    if len(targets) == 0:
        targets.append(logdir + '/verbatim.log')
    print targets
    for target in targets:
        readfile(target, tofile, start, delta)    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--logdir", type=str, dest='logdir', help="The directory of verbatim log files.")
    parser.add_argument("-f", action="store_true", help="Output to stdout or to `output.log`.")
    parser.add_argument("starttime", type=int, help="What timestamp to begin grabbing.")
    parser.add_argument("delta", type=int, help="How long to grab for.")

    args = parser.parse_args()
    main(args.logdir, args.starttime, args.delta, args.f)
