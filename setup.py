#!/bin/python3
import sys
import os
from scripts import module_add_admin
from scripts import module_wireguard
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

#Create heavens-door server config
def create_server_config():
        try:
                ip = input("What is your server public IP address? ")
                global EndPoint = ip + ":54817"
                command = "wg genkey | tee " + dir + "/configs/privatekey | wg pubkey > " + dir + "/configs/publickey"
                tmp = subprocess.getoutput([command])
                global ServerPublicKey = open(dir + '/configs/publickey').read()
                global ServerPrivateKey = open(dir + '/configs/privatekey').read()
                ServerConfig = open(dir + "/scripts/server_config.py", "w")
                ServerConfig.write('UserAddress = \"' + UserAddress + '\"\nServerPublicKey = \"' + ServerPublicKey + '\"\nEndPoint = \"' + EndPoint + '\"\nServerPrivateKey = \"' + ServerPrivateKey + '\"')
                ServerConfig.close()
                return 0
        except:
                return 1

#Create Wireguard server config from heavens-door config file
def create_wg_server_config():
        try:
                module_wireguard.create_wg_server_config()
                command = "cp " + dir + "/configs/wghub.conf /etc/wireguard/wghub.conf"
                subprocess.check_output(command, shell=True)
                command = "wg-quick up wghub"
                subprocess.check_output(command, shell=True)
                return 0
        except:
                return 1

#Create admin user
def create_admin():
        name = input("What is your admin name? ")
        #ip = input("What is your admin ip? ")
        ip = UserAddress + "1"
        tg = input("What is your admin Telegram id? ")
        #config_name = input("What is your configuration file name? ")
        config_name = module_wireguard.create_new_config(name)
        return module_add_admin.add(name+":"+ip+":"+tg+":"+config_name)

#Create systemd daemon config
#God, save my soul
def create_systemd_config():
        try:
                SystemdConfig = open("/lib/systemd/system/heavens-door.service", "w")
                SystemdConfig.write("[Unit]\nDescription=0\n\n[Service]\nExecStart=sudo " + dir + "/new_bot.py\nType=idle\nRestart=always")
                SystemdConfig.close()
                subprocess.check_output("systemctl start heavens-door.service", shell=True)

                if "active (running)" in subprocess.getoutput("systemctl status heavens-door.service"):
                        return 0
                else:
                        return 1
        except:
                return 1

if create_server_config() == 0:
        print("[ * ] Heavens-door config file created successfully")

        if create_wg_server_config() == 0:
                print("[ * ] Wireguard server config created successfully")

                if create_admin() == 0:
                        print("[ * ] Admin user was added succesfully")

                        #There will be added creatio of daemon of heavens-door
                        print("[ + ] Installation completed")
                else:
                        print("[ - ] Error. Admin wasn't added. Try to do it with your own hands")
        else:
                print("[ - ] Error. Wireguard server config wasn't created. Try to do it with your own hands")
else:
        print("[ - ] Error. Heavens-door config file wasn't created. Try to do it with your own hands")

