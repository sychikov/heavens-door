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

        result = module_database.change("update users set status = \"" + str(statuses.FlagAnathemed) + "\" where tg = "+str(tg))

#Get ip from telergram id account
def get_ip(tg):
        try:
                example = module_database.get("select ip from users where tg="+str(tg))
                list_ip = ''.join(example).split("\n")
                return(list_ip)

        except:

                sys.exit()

#Use ip for block user by ip
def block_user(list_ip):
        try:
                for ip in list_ip:
                        subprocess.check_output("iptables -A FORWARD -s " + ip + " -j REJECT", shell=True)
        except:
                sys.exit()
#Return successful code

def by_tg(tg):
        if (str(check_status(tg)[0]) == str(statuses.FlagNotBlocked)) or (str(check_status(tg)[0]) == str(statuses.FlagBlocked)):
                block_user(get_ip(tg))
                change_status(tg)
                return 0
        else:
                return 1

#If user was anathemed before restart server, iptables lose his rules

#Anathem user by tg if it was anathemed
def anathem_if_was_blocked():
        ips_db = get_ips_anathemed_from_db()
        if ips_db != '':
                ips_iptables = get_anathemed_ips_from_iptables()
                for ip in ips_db:
                        if ip not in ips_iptables:
                                anathem_single_ip(ip)
                return 0
        else:
                return 1

def get_ips_anathemed_from_db():
        return module_database.get("select ip from users where status == " + str(statuses.FlagAnathemed))

def get_anathemed_ips_from_iptables():
        return subprocess.getoutput(["iptables -L | grep REJECT | awk '{print $4}'"])

def anathem_single_ip(ip):
        subprocess.check_output("iptables -A FORWARD -s " + ip + " -j REJECT", shell=True)
