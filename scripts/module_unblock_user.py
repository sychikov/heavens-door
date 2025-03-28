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
        result = module_database.change("update users set status = \"" + str(statuses.FlagNotBlocked) + "\" where tg = "+str(tg))

#Get ip from telergram id account
def get_ip(tg):
        try:
                example = module_database.get("select ip from users where tg="+str(tg))
                list_ip = ''.join(example).split("\n")
                return(list_ip)

        except:
                sys.exit()

#Use ip for block user by ip
def unblock_user(list_ip):
        try:
                for ip in list_ip:
                        subprocess.check_output("iptables -D FORWARD -s " + ip + " -j REJECT", shell=True)
        except:
                sys.exit()

def by_tg(tg):
        if str(check_status(tg)[0]) == str(statuses.FlagBlocked):
                unblock_user(get_ip(tg))
                change_status(tg)
                return 0
        else:
                return 1
