#!/bin/python3
import subprocess
import sys
from scripts import module_database
from scripts import statuses

def check_status(tg):

        example = module_database.get("select status from users where tg="+str(tg))
        example = ''.join(example).split("\n")
        return example

def change_status(tg):

        result = module_database.change("update users set status = \"" + str(statuses.FlagBlocked) + "\" where tg = "+str(tg))

#Get ip from telergram id account
def get_ip(tg):
         example = module_database.get("select ip from users where tg="+str(tg))
         list_ip = ''.join(example).split("\n")
         return(list_ip)

#Use ip for block user by ip
def block_user(list_ip):
         for ip in list_ip:
                subprocess.check_output("iptables -A FORWARD -s " + ip + " -j REJECT", shell=True)
                        #print("iptables -A FORWARD -s", ip, "-j REJECT")
#               print("Iptables error")
#Return successful code

def by_tg(tg):
        if str(check_status(tg)[0]) == str(statuses.FlagNotBlocked):
                block_user(get_ip(tg))
                change_status(tg)
#       print("User has been blocked")
                return 0
        else:
#       print("User cannot be blocked, because he is already blocked")
                return 1
