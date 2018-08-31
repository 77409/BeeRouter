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
        self.nodes = {}     # 节点池
        self.requests = {}  # 请求池

    def set_debug(self, mode=0):
        self.debug_mode = mode

    def debug(self, params):
        if self.debug_mode > 0:
            print(params)

    def dumps(self, params):
        self.debug(json.dumps(params))

    def ping(self, params, current=None):
        # import pdb ; pdb.set_trace()
        self.debug (params)
        data = json.loads(params)
        data["peerId"] =  self.peerID
        data["timestamp"] =  time.time()
        return json.dumps(data)

    def swap(self, params, current=None):
        self.debug(params)
        return json.dumps(self.nodes)

    def check(self, params, current=None):
        self.debug(params)
        request = json.loads(params)
        peerId = request["peerId"]
        if peerId in self.requests :
            return json.dumps(self.requests[peerId])
        return json.dumps({"result" : None})

    def connect(self, params, current=None):
        self.debug(params)
        request = json.loads(params)
        peerId = request["peerId"]
        target = request["target"]
        request["result"] = "ok"
        request["code"] = 0
        self.requests[target] = request
        return json.dumps({"result" : "ok", "code" : 0})

    def register(self, params, current=None):
        self.debug(params)
        self.debug(current.con.toString())
        try :
            request = json.loads(params)
            peerId = request["peerId"]
            self.nodes[peerId] = request
            result = "ok"
            code = 0
        except:
            result = "fail"
            code = -1
        data = {"result" : result, "code" : code}
        return json.dumps(data)


def init_server (port, peerID=None):

    status = 0
    ic = None
    try:
       ic = Ice.initialize(sys.argv)
       adapter = ic.createObjectAdapterWithEndpoints(
                         "ConeAdapter", "default -p %d" %( port))
       server_object = ConeServer()
       server_object.set_debug(2)
       adapter.add(server_object, Ice.stringToIdentity("CONE"))
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
