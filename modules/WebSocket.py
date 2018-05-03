
# LibreCarrier Protocol
# Autobahn/Twisted websocket
import json
import socket
from autobahn.twisted.websocket import WebSocketServerProtocol
from modules import Settings
from argon2 import PasswordHasher, exceptions
global server
global channels
global users
global args
args = Settings.get()
if args["password"] or args["password_hash"]:
    args["protected"] = True
else:
    args["protected"] = False
channels = []
clients = []

# Todo Manages Ban
class LibreClient(WebSocketServerProtocol):

    def __init__(self):
        global server, channels
        WebSocketServerProtocol.__init__(self)
        server = {
                "name": args["name"],
                "channels": channels
            } 
        self.port = 0
        self.plugged = False
        self.channel = ""
        self.creator = False
        self.protected = args["protected"]
        print(json.dumps(server))

    # On connect we check if the user was banned
    def onConnect(self, request):
        ip, port = self.transport.client
        print(ip + ":" + ' connected')
        clients.append(self)

    def communication(self, message):
        for client in clients:
            if client.channel == self.channel:
                #print(self.channel)
                #print message
                if client != self:
                    try:
                        client.sendMessage(str(message.encode("utf-8")))
                    except:
                        pass

    def login(self, message):
        # Put inside get_commands
        is_json = False
        try:
            message = json.loads(message)
            is_json = True
        except:
            if message == "who":
                self.sendMessage(json.dumps(server))
                return
            elif message == "channels":
                self.sendMessage(json.dumps(channels))
                return
            elif message == "clients":
                self.sendMessage(str(len(clients)))
                return
        if is_json:
            # Add Channel
            if "add" in message:
                if message["add"] not in channels:
                    channels.append(message["add"])
                    self.sendMessage(str("Created: " + message["add"]))
                    self.creator = True
                    self.plugged = True
                    self.channel = message["add"]
                else:
                    self.sendMessage(str("Already created: " + message["add"]))
                    return
            # Remove channel
            elif "remove" in message:
                if message["remove"] in channels:
                    channels.remove(message["remove"])
                    self.sendMessage(str("Removed:" + message["remove"]))
                else:
                    self.sendMessage(str("Already removed: " + message["remove"]))
                return
            # Connect to channel
            elif "connect" in message:
                if message["connect"] in channels:
                    self.plugged = True
                    self.channel = message["connect"]
                    print(str("Connected to :" + self.channel))
                    self.sendMessage(str("Connected to :" + self.channel))
                else:
                    print("Channel doesn't exists")
                return
        else:
            #print "---IgNoRe----"
            self.sendMessage(str({"error": "invalid command"}))
            #print "-------------"

    # On open we ask for a password
    def onOpen(self):
        # print("[INFO]: WebSocket connection open.")
        # TODO: Not Logged
        if self.protected:
            self.sendMessage(server["name"] + " -- Password ?")
        else:
            # TODO: Logged
            self.sendMessage(json.dumps(server))

    # On message we check for the password
    def onMessage(self, payload, isBinary):
        is_json = False
        # print(clients)
        # Todo Manage Binary
        if not isBinary:
            message = payload.decode("utf-8")
            # print(message)
            # Not Logged
            if self.protected:
                try:
                    message = json.loads(message)
                    is_json = True
                except:
                    pass
                if is_json:
                    # print("json")
                    # print(message)
                    if "password" in message:
                        self.protected = self.passwordChecker(message["password"], args["password"], args["password_hash"])
                    if not self.protected:
                        self.sendMessage(json.dumps(server))
                    else:
                        self.sendMessage(server["name"] + " -- Password ?")
                else:
                    self.sendMessage(server["name"] + " -- Password ?")
            # Logged
            else:
                # On Channel
                if self.plugged:
                    self.communication(message)
                else:
                # Login Menu
                    self.login(message)

    def passwordChecker(self,user_pass,server_pass,server_hash):
        protected = True
        # print("Password detected")
        if server_pass is not False and server_hash is False:
            if user_pass == server_pass:
                protected = False

        if server_hash is not False and server_pass is False:
            try:
                ph = PasswordHasher()
                ph.verify(server_hash,user_pass)
                protected = False
            except exceptions.VerifyMismatchError:
                protected = True

        return protected

    # On close, we remove user from approved list
    def onClose(self, wasClean, code, reason):
        ip, port = self.transport.client
        if code != 1006:
            print(ip + ": disconnected")
        if self in clients:
            clients.remove(self)
        if self.creator:
            channels.remove(self.channel)
            for client in clients:
                if self.channel == client.channel:
                    client.sendMessage("Disconnected");
