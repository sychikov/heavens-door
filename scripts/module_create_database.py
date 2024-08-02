#!/bin/python3
import subprocess
import os
from scripts import module_add_user

database_name = "origin"

#Create first table and add here zero user
def create_table_users(path):
        command = "sqlite3 " + path + " 'create table users (id int, name string, ip string, status int, tg string)'"
        print(command)
        subprocess.check_output(command, shell=True)

#Create second table and add here zero user
def create_table_time(path):
        command = "sqlite3 " + path + " 'create table time (id int, ip string, hours int, minutes int)'"
        print(command)
        subprocess.check_output(command, shell=True)

#Create third table.
def create_table_configs(path):
        command = "sqlite3 " + path + " 'create table configs (ip string, config_name string)'"
        print(command)
        subprocess.check_output(command, shell=True)

#Create third table
#def create_table_time(path):
        #command = "sqlite3 " + path + " 'create table chat (tg string, chatid string)'"
        #print(command)
        #subprocess.check_output(command, shell=True)

#Path for creating database
def create_path():
        global database_name
        path = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1]) + f"/database/{database_name}"

        if not os.path.exists(path):
                open(path, "w").close()
        return path

#Add zero user
#def add_zero_user(path):
#       module_add_user.add("admin:10.10.10.10:111111")

#Main function
def create():
        path = create_path()
#       print(path)
        create_table_users(path)
        create_table_time(path)
        create_table_configs(path)
#add_zero_user(path)
#dir = '/'.join(os.path.abspath(os.curdir).split("/")[:-1])+"/database/"
