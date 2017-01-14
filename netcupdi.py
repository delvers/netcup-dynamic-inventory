#!/usr/bin/python
import zeep
import socket
import argparse
import yaml

# username and password for scp webservice more:
# https://www.netcup-wiki.de/wiki/Server_Control_Panel_(SCP)#Webservice
cfg = yaml.load(open("passwd.cfg", "r+"))
username = cfg.get('username')
password = cfg.get('password')



# setup webservice client
wsdl = 'https://www.vservercontrolpanel.de/WSEndUser?wsdl'
client = zeep.Client(wsdl=wsdl)

## TODO #########
# - add more error handling for soap responses
# - split and test ip to speicify version
# - improve ux by accepting hostnames, short names and ids

# setup cli params
parser = argparse.ArgumentParser(
        description='Ansible dynamic inventory script for netcup scp (and also some kind of cli)')
parser.add_argument('-H','--human', action='store_true',
        help='makes the output more readable for human')
parser.add_argument('-l', '--list', action='store_true',
        help='list servers with id and full hostname')
parser.add_argument('--host', default='none',
        help='show additional attributes of the given server')
parser.add_argument("-c", type=str, choices=['start', 'stop'], dest='control',
                            help="starts or stops server, requires --host")
args = parser.parse_args()



# represents a Server in the scp of netcup
class Server:

    # gathers information by server id
    def __init__(self, nameid):
        self.srvid    = srvid
        self.ips      = client.service.getVServerIPs(username, password, srvid)
        self.hostname = socket.gethostbyaddr(self.ips[0])[0]
        self.state    = client.service.getVServerState(username, password, nameid)

    # stops the server
    def stop(self):
        if self.state == "online":
            result = client.service.stopVServer(username, password, self.srvid)
            if result.success:
                print("Server " + self.hostname + " will be stopped soon.")
            else:
                print("ERROR:" + result.message)
                exit(1)
        else:
            print("The server is allready offline")
            exit(1)

    # starts the server
    def start(self):
        if self.state == "offline":
            result = client.service.startVServer(username, password, self.srvid)
            if result.success:
                print("Server " + self.hostname + " will be started")
            else:
                print("ERROR:" + result.message)
                exit(1)
        else:
            print("The server is allready online")
            exit(1)


    def printme(self):
        if args.human:
            print("############################################")
            print("Hostname: " + self.name)
            print("ID:   " + self.nameid)
            print("State: " + self.state)
            print("IPs: ")
            print(self.ips)
        else:
            print('"' + self.nameid + '"' + ' : [ "' + self.name + '" ],')



# collect all avariable servers
serverIDs = client.service.getVServers(username, password)
servers = {}

# gather more information about each server
for srvid in serverIDs:
    server = Server(srvid)
    servers[server.hostname] = server

# implement functions required by ansible
def list_hosts():
    if args.human:

        # print for human
        for srv in servers.values():
            print("############################################")
            print("Hostname: " + srv.hostname)
            print("ID:       " + srv.srvid)
            print("State:   " + srv.state)
            print("IPs: ")
            print(srv.ips)

    else:
        # print for ansible
        print("{")
        for srv in servers.values():
            print('\t"' + srv.srvid + '"' + ' : [ "' + srv.hostname + '" ],')
        print("}")


def show_host(srv):
    if srv != None:
        print('{')
        print('\t"hostname"\t: "'+ srv.hostname + '",')
        print('\t"ipv4"    \t: "'+ srv.ips[0]   + '",')
        print('\t"ipv6"    \t: "'+ srv.ips[1]   + '",')
        print('\t"state"   \t: "'+ srv.state    + '",')
        print('}')
    else:
        print "Server not found!"
        exit(1)

# run functions
if args.list:
    list_hosts()
elif args.host != 'none':
    srv = servers.get(args.host)
    if args.control == 'start':
        srv.start()
    elif args.control == 'stop':
        srv.stop()
    else:
        show_host(srv)
else:
    parser.parse_args(["--help"])
