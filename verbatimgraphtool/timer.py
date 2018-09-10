import sys
sys.path.append('/home/osboxes/Documents/verbatimgraphtool')
from logger import *
from lib import *
from bitcoin import *
from bitcoin.net import *
from bitcoin.core import *
from bitcoin.messages import *
import logging

import time
from cStringIO import StringIO
from bisect import insort, bisect
from pprint import pprint as pp
from collections import defaultdict
import struct
import json 
import socket


# This file opens a log connection to the logserver and
# reads all logs looking for inv messages. Two minutes after
# first inv message for a particular transaction is received
# the dictionary of the propagation times is dumped to the
# file indicated by 'outf'. The parameter for how long
# to wait before dumping can also be modified on line 97

SelectParams('mainnet')
S_TO_US = 1000000.0

def parse_record(record):
    sid, log_type, timestamp, rest = log.deserialize_part(record)
    logk = type_to_obj[log_type].deserialize(sid, timestamp, rest)
    return sid, log_type, timestamp, logk

#def readinv(invf, manifest, manfile):
def readinv(invf):
    #json.dump(manifest, open(manfile + '-result', 'wb'))
    #print manifest['txs']
    #for tx in manifest['txs']:
        #manifest['txs'][tx] = [ manifest['txs'][tx] ]
    while True:
        length = invf.read(4)
        if length == '':
            break
        try:
            length, = struct.unpack('>I', length)
        except Exception as e:
            print (e)
            return
        record = invf.read(length)
 
    #for record in invf.read().splitlines():
        sid, log_type, timestamp, log = parse_record(record)
        try:
            msg = MsgSerializable.stream_deserialize(StringIO(log.bitcoin_msg))
        except:
            continue
        
        seen = set()
        if msg is None: continue
        if msg.command == 'inv':
            for cinv in msg.inv:
                #if b2lx(cinv.hash) in manifest['txs']:
                    #print b2lx(cinv.hash)
                    #d = manifest['txs'][b2lx(cinv.hash)]
                    #print d
                    #if len(d) == 1:
                    print ('[%s] Transaction' % time.time(), b2lx(cinv.hash), 'found!')  
                    print (log.timestamp/S_TO_US, log.handle_id,sid)
                    #print str(sid)+"+++++"+str(log.handle_id),b2lx(cinv.hash)
                    #sample.write("{},{}\n".format(str(sid)+"+++++"+str(log.handle_id),b2lx(cinv.hash)))
                    #d.append( [log.timestamp/S_TO_US, log.handle_id] )
                    #manifest['txs'][b2lx(cinv.hash)] = sorted(d, key=lambda x: x[0])
    #for tx in manifest['txs']:
        #print tx, len(manifest['txs'][tx])
    #json.dump(manifest, open(manfile + '-result', 'wb'), encoding='latin1')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='?', type=argparse.FileType('rb'), default=sys.stdin)
    #parser.add_argument('manifest', type=str)
    args = parser.parse_args()

    print args
    #manifest = json.load( open(args.manifest,'rb') )
    #readinv(args.f, manifest, args.manifest)
readinv(args.f)
    
