#!/bin/python3
import sys
import os
from scripts import module_add_admin
import subprocess

#Variables
UserAddress = "10.0.0."
ServerPublicKey = ""
ServerPrivateKey = ""
EndPoint = ""

#Path to our dir
dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])

#Create database
from scripts import module_create_database
module_create_database.create()

#Create server config
def create_server_config():
        try:
                ip = input("What is your server public IP address? ")
                global EndPoint = ip + ":54817"
                global ServerPublicKey = subprocess.getoutput(["wg genkey"])
                global ServerPrivateKey = subprocess.getoutput(["wg genkey"])
                ServerConfig = open(dir + "/scripts/server_config.py" , "w")
                ServerConfig.write('UserAddress = \"' + UserAddress + '\"\nServerPublicKey = \"' + ServerPublicKey + '\"\nEndPoint = \"' + EndPoint + '\"\nServerPrivateKey = \"' + ServerPrivateKey + '\"')
                ServerConfig.close()
                return 0
        except:
                return 1

#Create Wireguard server config. Yeah, it's a different thing
def create_wg_server_config():
        try:
                #do something idk, you're author there

                return 1
        except:
                return 0
#Create admin user
def create_admin():
        name = input("What is your admin name? ")
        ip = input("What is your admin ip? ")
        tg = input("What is your admin Telegram id? ")
        config_name = input("What is your configuration file name? ")
        return module_add_admin.add(name+":"+ip+":"+tg+":"+config_name)


if create_admin() == 0:
        print("Admin was added succesfully.")

print("Installation completed")
