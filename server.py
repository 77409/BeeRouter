#!/usr/bin/env python
# -*- coding: utf-8 -*-

import CONE
import json, time
import Ice
from traceback import print_exc as dump_stack


class ConeServer(CONE.Peer):
    def __init__(self):
        self.peerID = "server-mac"
        self.debug_mode  = 0

    def set_debug(self, mode=0):
        self.debug_mode = mode

    def debug(self, params):
        if self.debug_mode > 0:
            print(params)

    def dumps(self, params):
        self.debug(json.dumps(params))

    def ping(self, params, current=None):
        self.debug (params)
        data = json.loads(params)
        data["peerId"] =  self.peerID
        data["timestamp"] =  time.time()
        return json.dumps(data)

    def swap(self, params, current=None):
        self.debug(params)

    def connect(self, params, current=None):
        self.debug(params)

    def register(self, params, current=None):
        self.debug(params)


def init_server (port, peerID=None):

    status = 0
    ic = None
    try:
       ic = Ice.initialize(sys.argv)
       adapter = ic.createObjectAdapterWithEndpoints(
                         "ConeAdapter", "default -p %d" %( port))
       object = ConeServer()
       adapter.add(object, Ice.stringToIdentity("CONE"))
       adapter.activate()
       ic.waitForShutdown()
    except:
       dump_stack()
       status = 1

    if ic:
       # Clean up
       try:
           ic.destroy()
       except:
           dump_stack()
           status = 1

    return(status)


if __name__ == "__main__":
    import sys

    # port = sys.argv[1]
    port = int(sys.argv[1])
    init_server(port)
