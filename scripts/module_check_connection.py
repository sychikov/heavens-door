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

#New way to check connected peers
def get_active_ips():
        #Get all peers that have non-zero sent packages in COUNT table
        tmp = subprocess.getoutput(["iptables -L COUNT -v -n | awk '{print $1,$8}' | grep -Ev '^0 |Chain|pkts' | awk '{print $2}'"])
        ips = ''.join(tmp).split("\n")
        print(ips)
        #Set counters to zero for the next check
        tmp = subprocess.getoutput(["iptables -Z COUNT"])
        return ips

#New way to ckec connected peers but without set counter to zero
def get_active_ips_without_zero():
        #Get all peers that have non-zero sent packages in COUNT table
        tmp = subprocess.getoutput(["iptables -L COUNT -v -n | awk '{print $1,$8}' | grep -Ev '^0 |Chain|pkts' | awk '{print $2}'"])
        ips = ''.join(tmp).split("\n")
        print(ips)
        return ips

#New main fuction (used only from admin interface)
def all_peers():
        answer = ""
        ips = get_active_ips_without_zero()
        if "10.28.98" not in ips[0]:
                answer = "No one connected."
        else:
                for ip in ips:
                        answer = answer + str(ip) + " connected. \n"
        return answer

#Main function
#def by_tg(tg):
#    if check_mode(tg) == 1:
#            print(check_connection(get_ip(tg)))
#    else:
#            answer = ""
#            ips = get_ips()
#            check = 0
#            for ip in ips:
#                    if check_connection(str(ip)) == 0:
#                            check = 1
#                            answer = answer + str(ip) + " connected. \n"
#            if check == 0:
#                    answer = "No one connected."
#            return answer
