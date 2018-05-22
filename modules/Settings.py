# Arguments parsing
import argparse
import os
import ConfigParser
import socket

description = "Interconnect websockets clients"
settings_file = "settings/librecarrier.ini"
VERSION = "0.8"

def get():
    args = get_from_terminal()
    args["server_ip"] = socket.gethostbyname(socket.gethostname())
    port = str(args["port"])
    if args["ssl"]:
        args["web_url"] = "https://" + args["server_ip"] + ":" + port
        args["ws_url"] = "wss://" + args["server_ip"] + ":" + port + "/ws"
    else:
        args["web_url"] = "http://" + args["server_ip"] + ":" + port
        args["ws_url"] = "ws://" + args["server_ip"] + ":" + port + "/ws"
    args["version"] = VERSION
    args = get_from_file(args)
    return args

def get_from_terminal():
    """ Get arguments list

    Returns:
        [args] -- an array of settings
    """

    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument("--offline", default=False, action="store_false",
                        help="Websocket is only available locally")
    parser.add_argument("--port", default=42000,
                        help="Port (default 42000)")
    parser.add_argument("--ssl", default=False, action="store_true",
                        help="Encrypt communication using SSL certificates")
    parser.add_argument("--nogui", default=False, action="store_true",
                        help="Enable gui")
    parser.add_argument("--password", default=False,
                        help="Password for the websocket")
    parser.add_argument("--password_hash", default=False,
                        help="Hashed password for websocket")
    parser.add_argument("--ip_ban_duration", default=0,
                        help="Seconds before a banned IP is unbanned")
    parser.add_argument("--ip_ban_retry", default=10,
                        help="Number of wrong password before IP is banned")
    parser.add_argument("--max_clients", default=False,
                        help="Number of clients")
    parser.add_argument("--certs", default="certs/",
                        help="location of the SSL certificates")
    parser.add_argument("--settings_file", default=settings_file,
                        help="Setting file location")
    parser.add_argument("--name", default="libreconnect")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Debug Mode")
    args = vars(parser.parse_args())
    if args["debug"] is True:
        print("Arguments -------------")
        print(args)
    return args


def get_from_file(args_cmd):
    """ Get arguments from a INI Configuration File

    Arguments:
        args {[string]} -- An array previously parsed from command line

    Returns:
        args {[string]} -- Returns arguments
    """
    if os.path.isfile(args_cmd["settings_file"]):
        file = ConfigParser.ConfigParser()
        file.read(args_cmd["settings_file"])
        for name, arg in args_cmd.items():
            try:
                args_cmd[name] = file.get("settings", name)
            except ConfigParser.NoOptionError:
                pass
        if args_cmd["debug"] is True:
            print("Configuration File -------------")
            print(args_cmd)
    return args_cmd
