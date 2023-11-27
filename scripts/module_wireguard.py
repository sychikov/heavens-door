#!/bin/python3
import subprocess
import sys
import os
from scripts import module_database
from scripts import server_config
#import pathlib

#dir.replace("scripts", "database"[, 1])
dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])

#Get config name from ip.
def get_names(ips):
    names = []
    for ip in ips:
         tmp = module_database.get("select config_name from configs where ip=\""+ip+"\"")
         #print("select config_name from configs where ip=\""+ip+"\"")
         #print(tmp)
         names.append(tmp)
         #names = ''.join(example).split("\n")
    return(names)

#Get server config info.
def get_server_config():
    server_config_str = "UserAddress = " + server_config.UserAddress + "*\nServerPublicKey = " + server_config.ServerPublicKey + " \nEndPoint = " + server_config.EndPoint + "\nServerPrivateKey = " + server_config.ServerPrivateKey
    return server_config_str

#Create Wireguard server config
def create_wg_server_config():
        try:
                #Probably will return with the next line symbol, be careful
                DefaultInterface = subprocess.getoutput("ip route list default | awk {'print $5'}")
                ServerWgConfig = open(dir + "/configs/wghub.conf")
                ServerWgConfig.write("\#Maden by Heavens door\n[Interface]\nAddress = 10.0.0.1/24\nListenPort = 54817\nPrivateKey = " + server_config.ServerPrivateKey + "\nSaveConfig = false\nMTU = 1280\nPostUp = iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -o " + DefaultInterface + " -j TCPMSS --clamp-mss-to-pmtu\nPostUp = iptables -t nat -A POSTROUTING -o " + DefaultInterface + " -j MASQUERADE\nPostDown = iptables -D FORWARD -i %i -j ACCEPT\nPostDown = iptables -t nat -D POSTROUTING -o " + DefaultInterface + " -j MASQUERADE\nPostDown = iptables -t mangle -D POSTROUTING -p tcp --tcp-flags SYN,RST SYN -o " + DefaultInterface + " -j TCPMSS --clamp-mss-to-pmtu\nPostUp = sysctl -q -w net.ipv4.ip_forward=1\nPostDown = sysctl -q -w net.ipv4.ip_forward=0")
                ServerWgConfig.close()
                return 0
        except:
                return 1

#Get config from it's name
def get_config(name):
        try:
            path = dir + "/configs/" + name
            config = open(path).read()
            #print(config)
            return config
        except:
            return 1

#Ultimate function that can create brand new configs
def create_new_config(name):
    command = "wg genkey | tee " + dir + "/configs/privatekey | wg pubkey > " + dir + "/configs/publickey"
    tmp = subprocess.getoutput([command])
    command = "wg genpsk > " + dir + "/configs/presharedkey"
    tmp = subprocess.getoutput([command])
    presharedkey = open(dir + '/configs/presharedkey').read()
    #privatekey = subprocess.getoutput(["cat " + dir + "/configs/privatekey"])
    privatekey = open(dir + '/configs/privatekey').read()
    #publickey = subprocess.getoutput(["cat " + dir + "/configs/publickey"])
    publickey = open(dir + '/configs/publickey').read()
    UserCounter = open(dir + '/configs/.user_counter').read()
    brand_new_config = "[Interface]\nAddress = " + server_config.UserAddress + str(int(UserCounter)+1) + "/24" + "\nDNS = 1.1.1.1\nPrivateKey = " + privatekey + "\n[Peer]\nPublicKey = " + server_config.ServerPublicKey + "\nPresharedKey = " + presharedkey + "AllowedIPs = 0.0.0.0/0\nEndpoint = " + server_config.EndPoint + "\n"

    #Add one point to user counter for future configs
    UserCounterFile = open(dir + '/configs/.user_counter', 'w')
    UserCounterFile.write(str(int(UserCounter)+1))
    UserCounterFile.close()

    #Create config file
    ConfigFile = open(dir + '/configs/wgclient_' + name + ".conf", 'w')
    ConfigFile.write(brand_new_config)
    ConfigFile.close()

    #Add new client to Wireguard server config
    WireguardConfigFile = open(dir + '/configs/wghub.conf', 'a')
    brand_new_config = "\n# " + str(int(UserCounter)+1) + " wgclient_" + name + ".conf\n[Peer]\nPublicKey = " + publickey + "PresharedKey = " + presharedkey + "AllowedIPs = " + server_config.UserAddress + str(int(UserCounter)+1) + "/32\n"
    WireguardConfigFile.write(brand_new_config)
    WireguardConfigFile.close()

    tmp = subprocess.getoutput(["wg-quick down wghub"])
    tmp = subprocess.getoutput(["cp " + dir + "/configs/wghub.conf /etc/wireguard/wghub.conf"])
    tmp = subprocess.getoutput(["wg-quick up wghub"])

    return "wgclient_" + name + ".conf"
