# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Simple echo server that echoes back client input.

You can run this .tac file directly with:
    twistd -ny telnet_echo.tac

This demo sets up a listening port on 6023 which accepts telnet connections.
No login for the telnet server is required.
"""

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory
from twisted.application.internet import TCPServer
from twisted.application.service import Application

class TelnetEcho(TelnetProtocol):
    def enableRemote(self, option):
        self.transport.write(b"You tried to enable " + option + b" (I rejected it)\r\n")
        return False


    def disableRemote(self, option):
        self.transport.write(b"You disabled " + option + b"\r\n")


    def enableLocal(self, option):
        self.transport.write(b"You tried to make me enable " + option + b" (I rejected it)\r\n" % (option,))
        return False


    def disableLocal(self, option):
        self.transport.write(b"You asked me to disable " + option + "\r\n")


    def dataReceived(self, data):
        self.transport.write(b"I received "+ data + b" from you\r\n")


factory = ServerFactory()
factory.protocol = lambda: TelnetTransport(TelnetEcho)
service = TCPServer(8023, factory)

application = Application("Telnet Echo Server")
service.setServiceParent(application)
