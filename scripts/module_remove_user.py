#!/bin/python3
from scripts import module_database

#Input should look like: "/remove_user *ip*"

#remove user from database
def remove_from_database(ip):
        try:
                result = module_database.change("delete from users where ip = \"" + ip + "\"")
                result = module_database.change("delete from time where ip = \"" + ip + "\"")
                return 0
        except:
                return 1
        #print("insert into users values (" + str(number) + ", \"" + user[0] + "\", \"" + user[1] + "\", " + " 0, \"" + user[2] + "\")")
        #print(result)

#Main function
def remove(ip):
        if remove_from_database(ip) == 0:
                return 0
        else:
                return 1


#print(remove("10.10.10.10"))
