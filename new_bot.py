#!/bin/python3
import time as imported_time
#Delay for previous bot stopped working
#imported_time.sleep(5)

import os

import requests
#Prepare path to bot token
main_path = os.path.dirname(os.path.abspath(__file__))
#Get bot token from file
token = open(main_path+'/.bot_token').read()
import telebot
import subprocess
from telebot import types

#Create bot with token
bot = telebot.TeleBot(token, threaded=False)

#Prepare user keyboard
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
butt_time = types.KeyboardButton('/time')
butt_status = types.KeyboardButton('/status')
butt_unblock = types.KeyboardButton('/unblock')
butt_configs = types.KeyboardButton('/configs')

#Create user keyboard
markup.row(butt_time, butt_status, butt_unblock, butt_configs)

import sys
#Import modules from scripts directory
from scripts import module_block_user
from scripts import module_unblock_user
from scripts import module_check_connection
from scripts import module_database
from scripts import module_anathem_user
from scripts import module_mercy_user
from scripts import module_add_user
from scripts import module_remove_user
from scripts import module_control_disturbers
from scripts import module_control_time
from scripts import module_broadcast
from scripts import module_wireguard
from scripts import statuses


#I use it for respawn bot if it'll fall'
def spawn_bot(token):
        return telebot.TeleBot(token, threaded=False)

#Get all clients from database
def get_clients():
        #tg = subprocess.getoutput(["sqlite3 /root/database/origin 'select tg from users'"])
        tg = module_database.get("select tg from users")
        tg = ''.join(tg).split("\n")
        tg = [tmp.split(" ")[0] for tmp in tg]
        return tg

#Get ips from telegram id
def get_my_ips(tg):
        #ips = subprocess.getoutput(["sqlite3 /root/database/origin 'select ip from users where tg = \"" + str(tg) + "\"'"])
        ips = module_database.get("select ip from users where tg = \"" + str(tg) + "\"")
        ips = ''.join(ips).split("\n")
        ips = [tmp.split(" ")[0] for tmp in ips]
        return ips

#Get hours and minutes of active work of client from ip
def get_my_time(ip):
        #hours = subprocess.getoutput(["sqlite3 /root/database/origin 'select hours from time where ip = \"" + str(ip) + "\"'"])
        #minutes = subprocess.getoutput(["sqlite3 /root/database/origin 'select minutes from time where ip = \"" + str(ip) + "\"'"])
        hours = module_database.get("select hours from time where ip = \"" + str(ip) + "\"")
        minutes = module_database.get("select minutes from time where ip = \"" + str(ip) + "\"")
        return "You active " + hours + " hours " + minutes + " minutes."

#get status about blocking
def get_my_status(ip):
        #status = subprocess.getoutput(["sqlite3 /root/database/origin 'select time from users where ip = \"" + str(ip) + "\"'"])
        status = module_database.get("select status from users where ip = \"" + str(ip) + "\"")
        status = ''.join(status).split("\n")
        return status[0]

#Unblock user by teleram id
def unblock_user(tg):
        result = module_unblock_user.by_tg(tg)
        if result == 0:
                return "User unblocked successfully"
        else:
                return "User cannot be unblocked"

#Chech if user is admin, user or noone
def check_rights(user_id):
        #master_code = subprocess.getoutput(["sqlite3 /root/database/origin 'select tg from users where id = 0'"])
        master_code = module_database.get("select tg from users where id = 0")
        master_code = ''.join(master_code)
        if user_id == int(master_code):
                return 0
        else:
            list_of_users = get_clients()
            for tg in list_of_users:
                if user_id == int(tg):
                    return 1
            return 2

#Start function for bot.
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "Hey buddy do you need something?\nUse command \"/help\" if you forgot commands", reply_markup=markup)
        #module_chat.check(user_id, message.chat.id)

    elif check_rights(user_id) == 2:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#    else:
#        send_msg_updt(user_id, "/help - show all commands. \n\nGet info: \n/show_users - show all users table. \n/show_time - show all users time table. \n/show_configs - show all configs table. \n/get_configs *tg* - get all configs associated with tg id. \n/check_connection - show connections of *all* or by tg id. \n\nContact with users: \n/broadcast *message* - send message to all users in database. \n/message *tg* *message* - send message to specified by tg user. \n\nControl user's activity: \n/easy_add *name*:*tg* - add user by easy way with only name and telegram id. \n/block_user *tg* - block user if it's possible, check the status table. \n/unblock_user *tg* - unblock user if it's possible, check the status table. \n/add_new_user *name*:*ip*:*tg*:*config_name* - add new user in database. \n/remove_user *ip* - remove user from database by ip. \n/anathem_user *tg* - eternal curse on user. \n/mercy_user *tg* - mercy user from eternal curse. \n\nWireguard commands: \n/create_new_config *config_name* - create brand new config for Wireguard and activate it (15 symbols max). \n/get_server_config - get server config file. ")
    elif check_rights(user_id) == 0:
        send_msg_updt(user_id, "/help - show all commands. \n\nGet info: \n/show_users - show all users table. \n/show_time - show all users time table. \n/show_configs - show all configs table. \n/get_configs *tg* - get all configs associated with tg id. \n/check_connection - show connections of *all* or by tg id. \n\nContact with users: \n/broadcast *message* - send message to all users in database. \n/message *tg* *message* - send message to specified by tg user. \n\nControl user's activity: \n/easy_add *name*:*tg* - add user by easy way with only name and telegram id. \n/block_user *tg* - block user if it's possible, check the status table. \n/remove_peer *ip* - remove peer from database and from server config by ip. \n/anathem_user *tg* - eternal curse on user. \n/mercy_user *tg* - mercy/unblock user and update database. \n\nWireguard commands: \n/get_server_config - get server config file. ")

#Admin function for get all table with users.
@bot.message_handler(commands=['show_users'])
def show_users(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        #new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from users'"])
        new_message = module_database.get("select * from users")
        send_msg_updt(user_id, new_message)
        #module_chat.check(user_id, message.chat.id)
    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#@bot.message_handler(commands=['show_status'])
#def show_status(message):
#    user_id = message.from_user.id
#    if  check_rights(user_id) == 0:
#        new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from user_status'"])
#        send_msg_updt(user_id, new_message)
#    elif check_rights(user_id) == 1:
#        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
#    else:
#        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for block user by his tg id.
@bot.message_handler(commands=['block_user'])
def block_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_block_user.by_tg(mess[1])
        #if result.split("\n")[0] == "0":
        #    send_msg_updt(user_id, "User blocked successfully")
        #else:
        #    send_msg_updt(user_id, "User cannot be blocked")
        if result == 0:
            send_msg_updt(user_id, "User blocked successfully")
        else:
            send_msg_updt(user_id, "User cannot be blocked")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin fucntion for unblock user by his tg id.
#@bot.message_handler(commands=['unblock_user'])
#def unblock_user(message):
#    user_id = message.from_user.id
#    if  check_rights(user_id) == 0:
#        mess = message.text.split(" ")
#        result = module_unblock_user.by_tg(mess[1])
#        if result == 0:
#            send_msg_updt(user_id, "User unblocked successfully")
#        else:
#            send_msg_updt(user_id, "User cannot be unblocked")

        #if result.split("\n")[0] == "0":
            #send_msg_updt(user_id, "User unblocked successfully")
        #else:
            #send_msg_updt(user_id, "User cannot be unblocked")

#    elif check_rights(user_id) == 1:
#        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
#    else:
#        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin fuction for check current connections. It pings all ips and see if anyone respond
@bot.message_handler(commands=['check_connection'])
def check_connection(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        if " " in message.text:
            mess = message.text.split(" ")
            result = module_check_connection.by_tg(mess[1])
        else:
            result = module_check_connection.by_tg("all")
        send_msg_updt(user_id, result)
    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for superblock user if he did something really bad. Only admin can cancel it.
@bot.message_handler(commands=['anathem_user'])
def anathem_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_anathem_user.by_tg(mess[1])
        #if result.split("\n")[0] == "0":
        #    send_msg_updt(user_id, "User blocked successfully")
        #else:
        #    send_msg_updt(user_id, "User cannot be blocked")
        if result == 0:
            send_msg_updt(user_id, "User anathemed successfully")
        else:
            send_msg_updt(user_id, "User cannot be anathemed")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for unblock superblocked user. Only way to cancel it.
@bot.message_handler(commands=['mercy_user'])
def mercy_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_mercy_user.by_tg(mess[1])
        if result == 0:
            send_msg_updt(user_id, "User unblocked successfully")
        else:
            send_msg_updt(user_id, "User cannot be unblocked")

        #if result.split("\n")[0] == "0":
            #send_msg_updt(user_id, "User unblocked successfully")
        #else:
            #send_msg_updt(user_id, "User cannot be unblocked")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for get all table with time and ips of all users.
@bot.message_handler(commands=['show_time'])
def get_all_time(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        #new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from users'"])
        new_message = module_database.get("select * from time")
        send_msg_updt(user_id, new_message)
    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for get all table with ips and configs.
@bot.message_handler(commands=['show_configs'])
def get_all_time(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        #new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from users'"])
        new_message = module_database.get("select * from configs")
        send_msg_updt(user_id, new_message)
    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#@bot.message_handler(commands=['show_configs1'])
#def get_all_time(message):
#    user_id = message.from_user.id
#    if  check_rights(user_id) == 0:
#        ips = get_my_ips(user_id)
#        names = module_wireguard.get_names(ips)
#        for name in names:
#            tmp = module_wireguard.get_config(name)
#            send_msg_updt_with_menu(user_id, tmp)
#    elif check_rights(user_id) == 1:
#        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
#    else:
#        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#User function for get his configs by tg id. Collect all his ips and return all files that associated with him.
@bot.message_handler(commands=['configs'])
def my_status(message):
    user_id = message.from_user.id
    if  (check_rights(user_id) == 1) or (check_rights(user_id) == 0):
        ips = get_my_ips(user_id)
        names = module_wireguard.get_names(ips)
        for name in names:
            tmp = module_wireguard.get_config(name)
            send_file_updt_with_menu(user_id, tmp)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin fucntion for get all configs from tg id.
@bot.message_handler(commands=['get_configs'])
def my_status(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        try:
            tg_id = mess[1]
            ips = get_my_ips(tg_id)
            names = module_wireguard.get_names(ips)
            for name in names:
                tmp = "`" + module_wireguard.get_config(name) + "`"
                send_msg_updt_with_menu_and_markdown(user_id, tmp)
        except:
            send_msg_updt_with_menu_and_markdown(user_id, "You sent no user tg")
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin fucntion for send message to all users who ever send "start" command to bot.
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        broadcast_message = ""
        for i in range(1,len(mess)):
            broadcast_message = broadcast_message + " " + mess[i]

        users_list = module_broadcast.get_clients()
        #print(users_list)
        for user_id in users_list:
            try:
                send_msg_updt_with_menu(user_id, broadcast_message)
                #print(broadcast_message)
            except:
                print("Message to " + user_id + " wasn't delivered.")
        #if result.split("\n")[0] == "0":
        #    send_msg_updt(user_id, "User blocked successfully")
        #else:
        #    send_msg_updt(user_id, "User cannot be blocked")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admins fucntion for send message to user by using his tg id. You can't send message to user that didn't asked "start" to bot.
@bot.message_handler(commands=['message'])
def new_message(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        print(mess)
        user_id = mess[1]
        new_message = ""
        for i in range(2,len(mess)):
            new_message = new_message + " " + mess[i]

        try:
            send_msg_updt_with_menu(user_id, new_message)
            #print(new_message)
        except:
            print("Message to " + user_id + " wasn't delivered.")
        #if result.split("\n")[0] == "0":
        #    send_msg_updt(user_id, "User blocked successfully")
        #else:
        #    send_msg_updt(user_id, "User cannot be blocked")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for create new user that will be added to users, time and config tables. It's more about specific config than client.
@bot.message_handler(commands=['easy_add'])
def easy_add(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_add_user.easy_add(mess[1])
        if result == 0:
            send_msg_updt(user_id, "User added successfully")
        else:
            send_msg_updt(user_id, "User cannot be added")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function for remove user from users, time and config tables by his ip. It's more about specific config than client.
@bot.message_handler(commands=['remove_peer'])
def remove_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_remove_user.remove(mess[1])
        #if result.split("\n")[0] == "0":
        #    send_msg_updt(user_id, "User blocked successfully")
        #else:
        #    send_msg_updt(user_id, "User cannot be blocked")
        if result == 0:
            send_msg_updt(user_id, "User removed successfully")
        else:
            send_msg_updt(user_id, "User cannot be removed")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")


#Admin function for create new configs and activate it by one command.
#@bot.message_handler(commands=['create_new_config'])
#def remove_user(message):
#    user_id = message.from_user.id
#    if  check_rights(user_id) == 0:
#        mess = message.text.split(" ")
#        config_name = mess[1]
#        config_name = config_name.split(".")
#        if len(config_name[0]) > 15:
#            send_msg_updt_with_menu(user_id, "Too long name, make it less than 15 symbols", reply_markup=markup)
#        else:
#            tmp = module_wireguard.create_new_config(mess[1])
#            send_msg_updt(user_id, tmp)
#
#    elif check_rights(user_id) == 1:
#        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
#    else:
#        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Admin function get server config file.
@bot.message_handler(commands=['get_server_config'])
def get_server_config(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        tmp = module_wireguard.get_server_config()
        send_msg_updt(user_id, tmp)

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Universal help command for users and for admin. More for admin, it's a lot of possible commands and no menu for him.
@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        markup = types.ReplyKeyboardMarkup()
        butt_time = types.KeyboardButton('/time')
        butt_status = types.KeyboardButton('/status')
        butt_unblock = types.KeyboardButton('/unblock')
        butt_configs = types.KeyboardButton('/configs')
        markup.row(butt_time, butt_status, butt_unblock, butt_configs)
        send_msg_updt_with_menu(user_id, "/help - show all commands. \n/unblock - unblock user if it's possible. \n/time - show your active time. \n/status - show your status. \n/configs - show your configs.", reply_markup=markup)
        #module_chat.check(user_id, message.chat.id)

#    elif check_rights(user_id) == 0:
#        send_msg_updt(user_id, "/help - show all commands. \n\nGet info: \n/show_users - show all users table. \n/show_time - show all users time table. \n/show_configs - show all configs table. \n/get_configs *tg* - get all configs associated with tg id. \n/check_connection - show connections of *all* or by tg id. \n\nContact with users: \n/broadcast *message* - send message to all users in database. \n/message *tg* *message* - send message to specified by tg user. \n\nControl user's activity: \n/easy_add *name*:*tg* - add user by easy way with only name and telegram id. \n/block_user *tg* - block user if it's possible, check the status table. \n/unblock_user *tg* - unblock user if it's possible, check the status table. \n/add_new_user *name*:*ip*:*tg*:*config_name* - add new user in database. \n/remove_user *ip* - remove user from database by ip. \n/anathem_user *tg* - eternal curse on user. \n/mercy_user *tg* - mercy user from eternal curse. \n\nWireguard commands: \n/create_new_config *config_name* - create brand new config for Wireguard and activate it (15 symbols max). \n/get_server_config - get server config file. ")
    elif check_rights(user_id) == 0:
        send_msg_updt(user_id, "/help - show all commands. \n\nGet info: \n/show_users - show all users table. \n/show_time - show all users time table. \n/show_configs - show all configs table. \n/get_configs *tg* - get all configs associated with tg id. \n/check_connection - show connections of *all* or by tg id. \n\nContact with users: \n/broadcast *message* - send message to all users in database. \n/message *tg* *message* - send message to specified by tg user. \n\nControl user's activity: \n/easy_add *name*:*tg* - add user by easy way with only name and telegram id. \n/block_user *tg* - block user if it's possible, check the status table. \n/remove_peer *ip* - remove peer from database and from server config by ip. \n/anathem_user *tg* - eternal curse on user. \n/mercy_user *tg* - mercy/unblock user and update database. \n\nWireguard commands: \n/get_server_config - get server config file. ")

    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#User command for get current time of activity of all his ip.
@bot.message_handler(commands=['time'])
def time(message):
    user_id = message.from_user.id
    if  (check_rights(user_id) == 1) or (check_rights(user_id) == 0):
        #module_chat.check(user_id, message.chat.id)
        ips = get_my_ips(user_id)
        for ip in ips:
            new_message = str(ip) + " " + get_my_time(ip)
            send_msg_updt_with_menu(user_id, new_message, reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#User command for get current status of all his ip.
@bot.message_handler(commands=['status'])
def my_status(message):
    user_id = message.from_user.id
    if  (check_rights(user_id) == 1) or (check_rights(user_id) == 0):
        new_message = ""
        ips = get_my_ips(user_id)
        for ip in ips:
            status = get_my_status(ip)
            #module_chat.check(user_id, message.chat.id)
            if str(status) == str(statuses.FlagBlocked):
                new_message = new_message + ip + " blocked.\n"
            elif str(status) == str(statuses.FlagNotBlocked):
                new_message = new_message + ip + " not blocked.\n"
            else:
                new_message = new_message + ip + " was anathemed. You did something really bad, contact your admininstrator or live with that curse.\n"
        send_msg_updt_with_menu(user_id, new_message, reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#user command for unblock himself if he was blocked by bot or admin. It won't work on superblocked users.
@bot.message_handler(commands=['unblock'])
def unblock_me(message):
    user_id = message.from_user.id
    if  (check_rights(user_id) == 1) or (check_rights(user_id) == 0):
        result = module_unblock_user.by_tg(user_id)
        #module_chat.check(user_id, message.chat.id)
        if result == 0:
            send_msg_updt_with_menu(user_id, "User unblocked successfully", reply_markup=markup)
        else:
            send_msg_updt_with_menu(user_id, "User cannot be unblocked", reply_markup=markup)
        #send_msg_updt_with_menu(user_id, new_message, reply_markup=markup)

#Answer for unknown command
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    if check_rights(user_id) == 0:
        send_msg_updt(user_id, "Unknown command, buddy\nTry /help or something")
    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "Unknown command, buddy\nTry /help or something", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")


#Admin function for add user and config easily
@bot.message_handler(commands=['easy_add'])
def easy_add(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_add_user.easy_add(mess[1])
        if result == 0:
            send_msg_updt(user_id, "User added successfully")
        else:
            send_msg_updt(user_id, "User cannot be added")

    elif check_rights(user_id) == 1:
        send_msg_updt_with_menu(user_id, "You have no rights for it", reply_markup=markup)
    else:
        send_msg_updt(user_id, "Fuck off man, I have a job to do")

#Thread for check users time, check if someone of them online for too long and block them if they deserved it.
def check_users_time():
    timerTillMessage = 0
    while True:
        module_control_time.check_time()
        module_control_disturbers.control()
        tgs = module_control_disturbers.get_edgers()
        #print(tgs)
        if tgs != 1:
            for user_id in tgs:
                try:
                    send_msg_updt(user_id[0], "Your connection will be blocked in 10 minutes. You're walking on the really thin ice, man.\n")
                except:
                    print("User with tg: "+user_id[0]+"; still didn't send to bot any messages")
        imported_time.sleep(600)
        #One more try to prevent bot from falling
        timerTillMessage = timerTillMessage + 10
        if timerTillMessage > 290:
            try:
                send_msg_updt("11111111", "Some message")
            except:
                print("Message was sent")
            timerTillMessage = 0

#Import library for catch exception below
from http.client import RemoteDisconnected

#Thread for respawn bot if that mf will fall.
def eternal_circle_of_pain():
    global bot
    try:
        bot.polling(none_stop=True)
    except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, requests.exceptions.ConnectionError, RemoteDisconnected):
        #print("ConnectionAbortedError")
        imported_time.sleep(2)
        bot.stop_polling()
        try:
            bot = spawn_bot(token)
        except:
            #I know that it's terrible desigion, but I have no another idea how to prevent bot from remote disconnection with TG servers.
            #subprocess.check_output("systemctl restart heavens-door.service", shell=True)
            print("Heavens door was just closed. But belive and they till be opened again.\n\n\n\n\n\n")
            sys.exit()

#Fix problem wirh falling bot after a 24 hours of work.
def send_msg_updt(telegram_id, msg):
    try:
        bot.send_message(telegram_id, msg)
    except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, ConnectionError):
        #print("ConnectionError - Sending again after 5 seconds!!!")
        imported_time.sleep(2)
        send_msg_updt(telegram_id, msg)

#Fix problem wirh falling bot after a 24 hours of work, but for regular clients.
def send_msg_updt_with_menu(telegram_id, msg, reply_markup=markup):
    try:
        bot.send_message(telegram_id, msg, reply_markup=markup)
    except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, ConnectionError):
        #print("ConnectionError - Sending again after 5 seconds!!!")
        imported_time.sleep(2)
        send_msg_updt_with_menu(telegram_id, msg, reply_markup=markup)

#Same stuff, but for file send
def send_file_updt_with_menu(telegram_id, config, reply_markup=markup):
    try:
        bot.send_document(telegram_id, config, reply_markup=markup)
    except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, ConnectionError):
        #print("ConnectionError - Sending again after 5 seconds!!!")
        imported_time.sleep(2)
        send_msg_updt_with_menu(telegram_id, msg, reply_markup=markup)

#Fix problem wirh falling bot after a 24 hours of work, but with markdown
def send_msg_updt_with_menu_and_markdown(telegram_id, msg):
    try:
        bot.send_message(telegram_id, msg, reply_markup=markup, parse_mode='MarkdownV2')
    except (ConnectionAbortedError, ConnectionResetError, ConnectionRefusedError, ConnectionError):
        #print("ConnectionError - Sending again after 5 seconds!!!")
        imported_time.sleep(2)
        send_msg_updt_with_menu_and_markdown(telegram_id, msg)


def update_firewall_rules():
    master_code = module_database.get("select tg from users where id = 0")
    master_code = ''.join(master_code)
    if module_anathem_user.anathem_if_was_blocked() == 0:
        send_msg_updt_with_menu(master_code, "Anathem list was updated successfully", reply_markup=markup)
    else:
        send_msg_updt_with_menu(master_code, "Error with updating anathem list", reply_markup=markup)
    if module_block_user.block_if_was_blocked() == 0:
        send_msg_updt_with_menu(master_code, "Block list was updated successfully", reply_markup=markup)
    else:
        send_msg_updt_with_menu(master_code, "Error with updating block list", reply_markup=markup)

#Main function

update_firewall_rules()
from threading import Thread
main_thread = Thread(target=check_users_time)
main_thread.daemon = True
secondary_thread = Thread(target=eternal_circle_of_pain)
main_thread.start()
secondary_thread.start()
