#!/usr/bin/env python
# -*- coding: utf-8 -*-

import CONE
import json
import Ice
import time
from traceback import print_exc as dump_stack


class Node():
    def __init__(self, host, port, my_peerId,  udp=False):
        self.my_peerId = my_peerId
        self.peerId = None
        self.ic = None
        self.base = None
        self.peer = None
        self.host = host
        self.port = port
        self.debug_mode = 0
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

    def set_debug(self, mode=0):
        self.debug_mode = mode

    def debug(self, params):
        if self.debug_mode > 0:
            print(params)

    def dumps(self, params):
        self.debug(json.dumps(params))

    def dump(self):
        print ("peerId : %s" % self.peerId)
        print ("host : %s" % self.host)
        print ("port : %d" % self.port)

    def _ping(self):
        data = {"peerId": self.my_peerId, "timestamp": time.time()}
        data = json.dumps(data)
        return json.loads(self.peer.ping(data))

    def ping(self):
        count = 4
        while count > 0:
            try :
                tick0 = time.time()
                ret = self._ping()
                tick1 = time.time()
                tick2 = ret["timestamp"]
                self.peerId = ret["peerId"]
                # self.replay = tick1- tick0
                # print( "from %s : arrival= %f ms, replay= %f ms" % (self.peerId, (tick2 - tick0 ) * 1000, (tick1 - tick0) * 1000))
                print( "from %s : arrival= %f ms, replay= %f ms" % (self.peerId, tick2 - tick0, tick1 - tick0 ) )
            except:
                print("ping failed!")
            count -= 1
            time.sleep(0.1)

    def register(self):
        data = { "peerId": self.my_peerId,  # peer ID
                 "transport": "udp"         # 传输类型 tcp / udp
                }
        data = json.dumps(data)
        ret = self.peer.register(data)
        ret = json.loads(ret)
        self.dumps(ret)
        return ret["code"]

    def check(self):
        data = {
                "peerId" : self.my_peerId,  # peer ID
                "sign" : "password"
            }
        data = json.dumps(data)
        ret = self.peer.check(data)
        self.debug (ret)
        return json.loads(ret)

    def swap(self):
        data = { "peerId": self.my_peerId}
        data = json.dumps(data)
        ret = self.peer.swap(data)
        self.debug(ret)

    def listen(self):
        while True:
            ret = self.check()
            if ret["result"] :
                break
            time.sleep(0.5)

    def connect(self, peerId):
        data = {
                "peerId": self.my_peerId,  # peer ID
                "target": peerId
            }
        data = json.dumps(data)
        ret = self.peer.connect(data)


def client(host, port, opr, peerId):
    node = Node(host, port, my_peerId = peerId)
    node.set_debug(1)
    node.ping()
    node.dump()

    if opr == 'register':
        node.register()
        node.listen()
    else:
        node.connect(peerId)


if __name__ == "__main__":
    import sys

    host = sys.argv[1]
    port = int(sys.argv[2])
    opr = 'register'
    try :
        opr = sys.argv[3]
        peerId = sys.argv[4]
    except:
        if opr and opr != 'register':
            raise RuntimeError("%s [host] [port] [register|connect] [peerId]" % (sys.argv[0]) )
        opr = 'register'
        peerId = None

    client(host, port, opr, peerId)
