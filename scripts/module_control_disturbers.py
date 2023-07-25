#!/bin/python3
import sys
import subprocess
import time
import collections
from scripts import module_database
from scripts import module_block_user
from scripts import statuses

#Check time of work of users. if someone work with vpn long enough, his ip will be returned
def check_disturbers():
        ips = module_database.get("select ip from time where hours > " + str(statuses.TimeLimit-1))
        ips = ''.join(ips).split("\n")
        ips = [tmp.split(" ")[0] for tmp in ips]
        return ips

#Get list of ips users that close to be blocked.
def check_edgers():
        ips = module_database.get("select ip from time where hours = " + str(statuses.TimeLimit-1) + " and minutes = 50")
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

bad_example = module_database.get("select ip from time where hours = -1")
bad_example = ''.join(bad_example).split("\n")
bad_example = [tmp.split(" ")[0] for tmp in bad_example]
bad_example = get_tgs(bad_example)

#Main function
def control():
        disturbers = get_tgs(check_disturbers())
        if disturbers:
                #print(len(disturbers[0]))
                print(bad_example)
                print(disturbers)
                if disturbers != bad_example:
                    block_disturbers(disturbers)

#Get list of edgers for send warning.
def get_edgers():
        edgers = get_tgs(check_edgers())
        if edgers:
                #print(len(disturbers[0]))
                #print(bad_example)
                #print(edgers)
                if edgers != bad_example:
                    return edgers
                else:
                    return 1

        #else:
                #print("No one to block(")
        #time.sleep(5)
