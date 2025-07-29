#!/bin/python3
from scripts import module_database
from scripts import statuses
from scripts import module_wireguard
import subprocess
user = [""]*4

#Input should look like: "/add_user name:ip:tg:config_name"
#Pase input for put it in database
def parse(new_user):
        global user
        count = 0
        for tmp in new_user.split(":"):
                #print(tmp)
                user[count] = tmp
                count = count + 1
        return 0

#Put user's data in database'
def add_to_database():
        global user
        if int(''.join(module_database.get("select count(id) from users").split("\n"))) == 0:
                number = 0
        else:
                number = int(''.join(module_database.get("select max(id) from users").split("\n")))+1
        result = module_database.change("insert into users values (" + str(number) + ", \"" + user[0] + "\", \"" + user[1] + "\", " + str(statuses.FlagNotBlocked) +",\"" + user[2] + "\")")
        result = module_database.change("insert into time values (" + str(number) + ", \"" + user[1] + "\", 0, 0)")
        result = module_database.change("insert into configs values (\"" + user[1] + "\", \"" + user[3] + "\")")
        #print("insert into users values (" + str(number) + ", \"" + user[0] + "\", \"" + user[1] + "\", " + " 0, \"" + user[2] + "\")")
        #print(result)

#Main function
def add(new_user):
        if parse(new_user) == 0:
                #try:
                add_to_database()
                return 0
                #except:
                          #return 1

        else:
                return 1

#Function for easily add user
#Input should look like: /easy_add name:tg
def easy_add(new_user):
        try:
                parsed_user = new_user.split(":")
                name = parsed_user[0]
                wg_info = module_wireguard.create_new_config(name)
                wg_info = wg_info.split("   ")

                config_name = wg_info[0]
                ip_address = wg_info[1]
                tg_num = parsed_user[1]

                number = int(''.join(module_database.get("select max(id) from users").split("\n")))+1

                result = module_database.change("insert into users values (" + str(number) + ", \"" + name + "\", \"" + ip_address + "\", " + str(statuses.FlagNotBlocked) +",\"" + tg_num + "\")")
                result = module_database.change("insert into time values (" + str(number) + ", \"" + ip_address + "\", 0, 0)")
                result = module_database.change("insert into configs values (\"" + ip_address + "\", \"" + config_name + "\")")
                tmp = subprocess.getoutput(["iptables -A COUNT -s " + ip_address + " -j RETURN"])
                return 0
        except:
                return 1

