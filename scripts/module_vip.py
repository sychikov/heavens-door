#!/bin/python3
from scripts import module_database
from scripts import statuses

#Grant user with divine blessing
def add_to_vip(tg):
        if check_vip_status(tg):
            return False
        else:
            try:
                result = module_database.change("update users set status = \"" + str(statuses.FlagVIP) + "\" where tg = "+str(tg))
                return True
            except:
                return False

#Check is user already have VIP status
def check_vip_status(tg):
        user_status = module_database.get("select status from users where tg="+str(tg))
        user_status = ''.join(user_status).split("\n")
        if (str(user_status[0]) == str(statuses.FlagVIP)):
                return True
        else:
                return False

#Delete user from VIP list
def delete_from_vip(tg):
        try:
            if check_vip_status(tg):
                result = module_database.change("update users set status = \"" + str(statuses.FlagNotBlocked) + "\" where tg = "+str(tg))
                return True
            else:
                return False
        except:
            return False
