#!/bin/python3
import subprocess
import sys
from scripts import module_database
answer = "1 packets transmitted, 1 received, 0% packet loss"

#Check mode of checking
def check_mode(mode):
        if mode == "all":
                return 0
        else:
                return 1

#Get ip from database
def get_ip(tg):
        tmp = module_database.get("select ip from users where tg="+tg)
        ip = ''.join(tmp)

#Get all Ips
def get_ips():
        tmp = module_database.get("select ip from users")
        ips = ''.join(tmp).split("\n")
        return ips

#Ping client for check his connection
def check_connection(ip):
        tmp = subprocess.getoutput(["ping -c 1 -w 1 "+ip])
        if answer in tmp:
                return 0
        else:
                return 1

#Main function
def by_tg(tg):
    if check_mode(tg) == 1:
            print(check_connection(get_ip(tg)))
    else:
            answer = ""
            ips = get_ips()
            check = 0
            for ip in ips:
                    if check_connection(str(ip)) == 0:
                            check = 1
                            answer = answer + str(ip) + " connected. \n"
            if check == 0:
                    answer = "No one connected."
            return answer
