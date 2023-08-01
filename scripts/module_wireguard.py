#!/bin/python3
import subprocess
import sys
import os
from scripts import module_database
#import pathlib

#dir.replace("scripts", "database"[, 1])
dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])

def get_names(ips):
    names = []
    for ip in ips:
         tmp = module_database.get("select config_name from configs where ip=\""+ip+"\"")
         #print("select config_name from configs where ip=\""+ip+"\"")
         #print(tmp)
         names.append(tmp)
         #names = ''.join(example).split("\n")
    return(names)

def get_config(name):
        try:
            path = dir + "/configs/" + name
            config = open(path).read()
            #print(config)
            return config
        except:
            return 1
