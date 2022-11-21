#!/bin/python3
import subprocess
import sys
import os
#import pathlib

#dir.replace("scripts", "database"[, 1])

def get(command):
        dir = '/'.join(os.path.abspath(os.curdir).split("/"))+"/database/"
        if "scripts/database" in dir:
                dir = '/'.join(os.path.abspath(os.curdir).split("/")[:-1])+"/database/"
        command = "sqlite3 " + dir + "origin '" + command +"'"
        return subprocess.getoutput([command])
        #return command
        #return command

def change(command):
        try:
                dir = '/'.join(os.path.abspath(os.curdir).split("/"))+"/database/"
                if "scripts/database" in dir:
                        dir = '/'.join(os.path.abspath(os.curdir).split("/")[:-1])+"/database/"
                command = "sqlite3 " + dir + "origin '" + command +"'"
                subprocess.check_output(command, shell=True)
                #print(command)
                return command
        except:
                return 1

#p = pathlib.Path('origin.database')
#print(p)
#print(get("select * from users;"))
#output([command])

