#!/bin/python3
import subprocess
import sys
import os
#import pathlib

#dir.replace("scripts", "database"[, 1])

def get(command):
        dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
        #if "scripts/" in dir:
                #dir = '/'.join(dir.split("/")[:-1])
        command = "sqlite3 " + dir + "/database/origin '" + command +"'"
        return subprocess.getoutput([command])
        #return command
        #return command

def change(command):
        try:
                dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
                #if "scripts/" in dir:
                        #dir = '/'.join(dir.split("/")[:-1])
                command = "sqlite3 " + dir + "/database/origin '" + command +"'"
                subprocess.check_output(command, shell=True)
                #print(command)
                return command
        except:
                return 1

#p = pathlib.Path('origin.database')
#print(p)
#print(get("select * from users;"))
#output([command])

