#!/bin/python3
from scripts import module_database
from scripts import statuses
user = [""]*3

#Input should look like: "/add_user name:ip:tg"
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

#add("cock:10.10.10.10:218378123")
