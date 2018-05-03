'''
LibreCarrier
Description ----------------------------------
LibreCarrier makes any websocket client into a private communication channel.
This allows to easily connect applications and electronic objects to a network.
----------------------------------------------
Author : Remi Sarrailh (madnerd.org)
Email : remi@madnerd.org
License : MIT
Based on this tutorial by Simply Automationized
https://simplyautomationized.blogspot.fr/2015/09/raspberry-pi-create-websocket-api.html
'''
from twisted.internet import protocol, reactor, ssl
from twisted.web.server import Site
from twisted.web.static import File
from twisted.python import log
import argparse
import ConfigParser
import os
import sys
import socket
import threading
# Arguments/ Time
import time
from autobahn.twisted.websocket import (WebSocketServerFactory,
                                        WebSocketServerProtocol, listenWS)
# Websocket
from modules import Settings
from modules.WebSocket import LibreClient
# Hashed password
import _cffi_backend  # Need for pyinstaller

# LibreConnect Protocol
from autobahn.twisted.websocket import (WebSocketServerProtocol)
from autobahn.twisted.resource import WebSocketResource
# Autobahn/Twisted websocket
import json

# Get parameters from terminal or settings file
args = Settings.get()

if args["gui"]:
    from modules import Gui

failed_start = False

print("LibreCarrier - version " + args["version"])
print("By madnerd.org (https://github.com/madnerdorg/librecarrier)")
print("----------------------------------------------------------")

if args["debug"] is True:
    print("Arguments -------------")
    print(args)

settings_text = ""
if args["ssl"]:
    settings_text = settings_text + "SSL "
    ws_type = "wss://"
else:
    ws_type = "ws://"

if args["offline"]:
    settings_text = settings_text + "OFFLINE "
    interface = "localhost"
else:
    interface = ""

if args["password"] or args["password_hash"]:
    settings_text = settings_text + "PASSWORD "

address = ws_type+"0.0.0.0"+":"+str(args["port"])

#############################
#      WebSocket Server     #
#############################
factory = WebSocketServerFactory(address)
if args["debug"] is True:
    log.startLogging(sys.stdout)

ssl_private = args["certs"] + "/privkey.pem"
ssl_public = args["certs"] + "/cert.pem"

if args["ssl"]:
    if os.path.isfile(ssl_private) and os.path.isfile(ssl_public):
        contextFactory = ssl.DefaultOpenSSLContextFactory(ssl_private,
                                                          ssl_public)
        # listenWS(factory, contextFactory, interface=interface)
        resource = WebSocketResource(factory)
    else:
        print("[ERROR]: I can't find " + ssl_private + " and/or " + ssl_public)
        failed_start = True
else:
    # listenWS(factory, interface=interface)
    resource = WebSocketResource(factory)

if not failed_start:
    print(ws_type + args["server_ip"] + ":" + str(args["port"]) + " " + settings_text)
    factory.protocol = LibreClient
    root = File("web/")
    root.putChild(b"ws", resource)
    site = Site(root)

    if args["ssl"]:
        reactor.listenSSL(int(args["port"]), site, contextFactory, interface=interface)
    else:
        reactor.listenTCP(int(args["port"]), site, interface=interface)
    reactor.run()
