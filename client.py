#!/usr/bin/env python
# -*- coding: utf-8 -*-

import CONE
import json
import Ice
import time
from traceback import print_exc as dump_stack


class Node():
    def __init__(self, host, port, my_peerId=None,  udp=False):
        self.my_peerId = my_peerId
        self.peerId = None
        self.ic = None
        self.base = None
        self.peer = None
        self.host = host
        self.port = port
        self.ice_init()

    def ice_init(self):
        try:
            self.ic = Ice.initialize([])
            self.base = self.ic.stringToProxy("CONE:default -h %s -p %d" % (self.host, self.port))
            self.peer = CONE.PeerPrx.checkedCast(self.base)
            if not self.peer:
                raise RuntimeError("Invalid proxy")
        except:
            dump_stack()
            status = 1

    def __del__(self):
        if self.ic:
            try:
                self.ic.destroy()
            except:
                dump_stack()

    def ping(self):
        count = 4
        while count > 0:
            try :
                tick0 = time.time()
                ret = json.loads(self.peer.ping(json.dumps({"peerId": self.my_peerId, "timestamp": time.time()})))
                tick1 = time.time()
                tick2 = ret["timestamp"]
                self.peerId = ret["peerId"]
                # self.replay = tick1- tick0
                print( "from %s : arrival=%fms,replay=%fms" % (self.peerId, tick2- tick0, tick1- tick0))
            except:
                print("ping failed!")
            count -= 1
            time.sleep(1)

def client(host, port):
    node = Node(host, port, my_peerId = "cdj-windows")
    node.ping()


if __name__ == "__main__":
    import sys

    host = sys.argv[1]
    port = int(sys.argv[2])
    client(host, port)
