#!/bin/python3
import sys
import subprocess
import time
from scripts import module_database
from scripts import module_check_connection

#Get all clients
def get_clients():

        ips = module_database.get("select ip from users")
        ips = ''.join(ips).split("\n")
        ips = [tmp.split(" ")[0] for tmp in ips]
        return ips

#Get clients that can be pinged
def get_active_clients():

        ips = module_check_connection.by_tg("all")
        ips = ''.join(ips).split("\n")
#       for tmp in ips:
#               tmp = str(tmp.split(" ")[0])
        ips = [tmp.split(" ")[0] for tmp in ips]
        return ips[:-1]

#Set time of inactive clients to zero
def set_zero_time(ip):
        result = module_database.change("update time set minutes = 0 where ip=\""+ip+"\"")

        result = module_database.change("update time set hours = 0 where ip=\""+ip+"\"")


#Add 10 monutes to active user
def add_time(ip):
        time = module_database.get("select minutes from time where ip=\""+ip+"\"")

        #time = int(time[:-1])
        time = int(''.join(time.split("\n")))
        if (time+10) >= 60:
                result = module_database.change("update time set minutes = " + str(time+10-60) + " where ip=\""+ip+"\"")
                time = int(module_database.get("select hours from time where ip=\""+ip+"\""))
                result = module_database.change("update time set hours = " + str(time+1) + " where ip=\""+ip+"\"")

        else:
                result = module_database.change("update time set minutes = " + str(time+10) + " where ip=\""+ip+"\"")

        print(ip + " " + module_database.get("select hours, minutes from time where ip=\""+ip+"\""))


#print(get_clients())
#Main function
def check_time():
        ips = get_active_clients()
        #print(ips)
        allip = get_clients()
        for ip in allip:
                if ip not in ips:
                        set_zero_time(ip)
                        print(ip + " inactive")

        for ip in ips:
                add_time(str(ip))
        #time.sleep(600)
