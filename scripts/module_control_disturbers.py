#!/bin/python3
import sys
import subprocess
import time
from scripts import module_database
from scripts import module_block_user

#Check time of work of users. if someone work with vpn long enough, his ip will be returned
def check_disturbers():
        ips = module_database.get("select ip from time where hours > 11")
        ips = ''.join(ips).split("\n")
        ips = [tmp.split(" ")[0] for tmp in ips]
        return ips

#Get telegram ids from list of ip disturbers
def get_tgs(ips):
        tgs = []
        for ip in ips:
                tg = module_database.get("select tg from users where ip = \"" + ip + "\"")
                tg = ''.join(tg).split("\n")
                if tg not in tgs:
                        tgs.append(tg)
        return tgs

#Block disturbers by their telegram ids
def block_disturbers(tgs):
        for tg in tgs:
                if module_block_user.by_tg(''.join(tg)) == 0:
                        print("User with tg " + str(tg) + " has been blocked succesfully")
                else:
                        print("User with tg " + str(tg) + " cannot be blocked")
#Main function
def control():
        disturbers = get_tgs(check_disturbers())
        if not disturbers:
                print(len(disturbers[0]))
                block_disturbers(disturbers)
        #time.sleep(5)
