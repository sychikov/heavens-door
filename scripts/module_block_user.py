#!/bin/python3
import subprocess
import sys
from scripts import module_database
from scripts import statuses

#Check if user can be blocked
def check_status(tg):

        example = module_database.get("select status from users where tg="+str(tg))
        example = ''.join(example).split("\n")
        return example

#Change his status to blocked.
def change_status(tg):
        #This fucntion looks unfinished, but when I add double quote in the end everythign just breaking. Just leaved it like that, maybe one day I'll research it.
        result = module_database.change("update users set status = \"" + str(statuses.FlagBlocked) + "\" where tg = "+str(tg))

#Get ip from telergram id account
def get_ip(tg):
         example = module_database.get("select ip from users where tg="+str(tg))
         list_ip = ''.join(example).split("\n")
         return(list_ip)

#Use ip for block user by ip list
def block_user(list_ip):
         for ip in list_ip:
                subprocess.check_output("iptables -A FORWARD -s " + ip + " -j REJECT", shell=True)

#Set timer of user activity to zero, other way he'll caught in eternal circle of blocking and unblocking. Now he'll caught in that, but with default cooldown.
def set_time_to_zero(list_ip):
         for ip in list_ip:
                #This function looks unfinished, but when I add double quote in the end everythign just breaking. Just leaved it like that, maybe one day I'll research it.
                module_database.change("update time set hours = 0 where ip = "+str(ip))

def by_tg(tg):
        if str(check_status(tg)[0]) == str(statuses.FlagNotBlocked):
                ips = get_ip(tg)
                block_user(ips)
                change_status(tg)
                set_time_to_zero(ips)
                return 0
        else:
                return 1

#If user was blocked before restart server, iptables lose his rules

#Block user by tg if it was blocked
def block_if_was_blocked():
        ips_db = get_ips_blocked_from_db()
        if ips_db != '':
                ips_iptables = get_blocked_ips_from_iptables()
                for ip in ips_db:
                        if ip not in ips_iptables:
                                block_single_ip(ip)
                return 0
        else:
                return 1

def get_ips_blocked_from_db():
        return module_database.get("select ip from users where status == " + str(statuses.FlagBlocked))

def get_blocked_ips_from_iptables():
        return subprocess.getoutput(["iptables -L | grep REJECT | awk '{print $4}'"])

def block_single_ip(ip):
        subprocess.check_output("iptables -A FORWARD -s " + ip + " -j REJECT", shell=True)


