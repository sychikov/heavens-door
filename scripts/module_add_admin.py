#!/bin/python3
from scripts import module_database
from scripts import statuses
admin = [""]*4

#Input should look like: "/add_admin name:ip:tg:config_name"
#Pase input for put it in database
def parse(new_admin):
        global admin
        count = 0
        for tmp in new_admin.split(":"):
                print(tmp)
                admin[count] = tmp
                count = count + 1
        return 0

#Put user's data in database'
def add_to_database():
        global admin
        #number = int(''.join(module_database.get("select max(id) from users").split("\n")))+1
        number = 0
        #result = module_database.change("update users set name = \"" + admin[0] + "\", ip = \"" + admin[1] + "\", tg = \"" + admin[2] + "\" where id = 0")
        #result = module_database.change("update time set ip = \"" + admin[1] + "\" where id = 0")
        #command = "insert into users values (0, \"" + admin[0] + "\", \"" + admin[1] + "\", 0, \"" + admin[2] + "\")"
        #print(command)
        #result = module_database.change(command)
        result = module_database.change("insert into users values (0, \"" + admin[0] + "\", \"" + admin[1] + "\", " + str(statuses.FlagNotBlocked) + ", \"" + admin[2] + "\")")
        result = module_database.change("insert into time values (0, \"" + admin[1] + "\", 0, 0)")
        result = module_database.change("insert into configs values (\"" + admin[1] + "\", \"" + admin[3] + "\")")
        #result = module_database.change("update time set ip = \"" + admin[1] + "\" where id = 0")
        #print("insert into admins values (" + str(number) + ", \"" + admin[0] + "\", \"" + admin[1] + "\", " + " 0, \"" + admin[2] + "\")")
        #print(result)

#Main function
def add(new_admin):
        if parse(new_admin) == 0:
                add_to_database()
                return 0
        else:
                return 1
