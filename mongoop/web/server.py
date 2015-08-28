# -*- coding: utf-8 -*-
"""
    mongoop.web.server
    ~~~~~~~~~~~~~~~~~~

    A simple webserver using Autobahn/WebSockets.

    :copyright: (c) 2015 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""

import logging

from sys import exit

from asyncio import get_event_loop

from autobahn.asyncio.websocket import WebSocketServerProtocol
from autobahn.asyncio.websocket import WebSocketServerFactory


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


class MongoopProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

class MongoopServer:

    def __init__(self, addr='127.0.0.1', port=9000, debug=False):
        try:
            self.addr = addr
            self.port = port
            self.debug = debug
            self.ws_addr = 'ws://{}:{}'.format(self.addr, self.port)

            self.factory = WebSocketServerFactory(self.ws_addr, debug=self.debug)
            self.factory.protocol = MongoopProtocol

            self.loop = get_event_loop()
            self.coro = self.loop.create_server(self.factory, '0.0.0.0', self.port)
            self.server = self.loop.run_until_complete(self.coro)
        except Exception as e:
            logging.warning('unable to run webserver :: {}'.format(e))
            exit(1)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # TODO: context manager?
            self.server.close()
            self.loop.close()


def main():
    server = MongoopServer()
    server.run()


if __name__ == '__main__':
    main()
