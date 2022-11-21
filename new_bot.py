#!/bin/python3

#Get bot token
token = open('.bot_token').read()

import telebot
import subprocess
from telebot import types

#Create bot
bot = telebot.TeleBot(token)

#Prepare user keyboard
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
butt_time = types.KeyboardButton('/time')
butt_status = types.KeyboardButton('/status')
butt_unblock = types.KeyboardButton('/unblock')
markup.row(butt_time, butt_status, butt_unblock)

#Import modules from scripts directory
import os
import sys
#base_dir = os.path.dirname(__file__) or '.'
#dir_scripts = os.path.join(base_dir, 'scripts')
#sys.path.append(dir_scripts)

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
from database import statuses

#Get all clients
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

#Chech if user is admin
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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        bot.send_message(user_id, "Hey buddy do you need something?\nUse command \"help\" if you forgot commands", reply_markup=markup)

    elif check_rights(user_id) == 2:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

    else:
        bot.send_message(user_id, "help - show all commands. \nshow_users - show all users table. \nblock_user *** - block user if it's possible, check the status table. \nunblock_user *** - unblock user if it's possible, check the status table. \ncheck_connection - show connections of *all* or by tg id. \nadd_new_user *name*:*ip*:*tg* - add new user in database. \nremove_user *ip* - remove user from database by ip. \nanathem_user *** - eternal curse on user. \n mercy_user *tg* - mercy user from eternal curse.")

@bot.message_handler(commands=['show_users'])
def show_users(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        #new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from users'"])
        new_message = module_database.get("select * from users")
        bot.send_message(user_id, new_message)
    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

#@bot.message_handler(commands=['show_status'])
#def show_status(message):
#    user_id = message.from_user.id
#    if  check_rights(user_id) == 0:
#        new_message = subprocess.getoutput(["sqlite3 /root/database/origin 'select * from user_status'"])
#        bot.send_message(user_id, new_message)
#    elif check_rights(user_id) == 1:
#        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
#    else:
#        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['block_user'])
def block_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_block_user.by_tg(mess[1])
        #if result.split("\n")[0] == "0":
        #    bot.send_message(user_id, "User blocked successfully")
        #else:
        #    bot.send_message(user_id, "User cannot be blocked")
        if result == 0:
            bot.send_message(user_id, "User blocked successfully")
        else:
            bot.send_message(user_id, "User cannot be blocked")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['unblock_user'])
def unblock_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_unblock_user.by_tg(mess[1])
        if result == 0:
            bot.send_message(user_id, "User unblocked successfully")
        else:
            bot.send_message(user_id, "User cannot be unblocked")

        #if result.split("\n")[0] == "0":
            #bot.send_message(user_id, "User unblocked successfully")
        #else:
            #bot.send_message(user_id, "User cannot be unblocked")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['check_connection'])
def check_connection(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_check_connection.by_tg(mess[1])
        bot.send_message(user_id, result)
    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['anathem_user'])
def block_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_anathem_user.by_tg(mess[1])
        #if result.split("\n")[0] == "0":
        #    bot.send_message(user_id, "User blocked successfully")
        #else:
        #    bot.send_message(user_id, "User cannot be blocked")
        if result == 0:
            bot.send_message(user_id, "User anathemed successfully")
        else:
            bot.send_message(user_id, "User cannot be anathemed")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['mercy_user'])
def unblock_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")
        result = module_mercy_user.by_tg(mess[1])
        if result == 0:
            bot.send_message(user_id, "User merced successfully")
        else:
            bot.send_message(user_id, "User cannot be merced")

        #if result.split("\n")[0] == "0":
            #bot.send_message(user_id, "User unblocked successfully")
        #else:
            #bot.send_message(user_id, "User cannot be unblocked")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['add_new_user'])
def block_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_add_user.add(mess[1])
        #if result.split("\n")[0] == "0":
        #    bot.send_message(user_id, "User blocked successfully")
        #else:
        #    bot.send_message(user_id, "User cannot be blocked")
        if result == 0:
            bot.send_message(user_id, "User added successfully")
        else:
            bot.send_message(user_id, "User cannot be added")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['remove_user'])
def block_user(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 0:
        mess = message.text.split(" ")

        result = module_remove_user.remove(mess[1])
        #if result.split("\n")[0] == "0":
        #    bot.send_message(user_id, "User blocked successfully")
        #else:
        #    bot.send_message(user_id, "User cannot be blocked")
        if result == 0:
            bot.send_message(user_id, "User removed successfully")
        else:
            bot.send_message(user_id, "User cannot be removed")

    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "You have no rights for it", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        markup = types.ReplyKeyboardMarkup()
        butt_time = types.KeyboardButton('/time')
        butt_status = types.KeyboardButton('/status')
        butt_unblock = types.KeyboardButton('/unlock')
        markup.row(butt_time, butt_status, butt_unblock)
        bot.send_message(user_id, "Hey buddy do you need something?\nUse command \"help\" if you forgot commands", reply_markup=markup)

    elif check_rights(user_id) == 0:
        bot.send_message(user_id, "help - show all commands. \nshow_users - show all users table. \nblock_user *** - block user if it's possible, check the status table. \nunblock_user *** - unblock user if it's possible, check the status table. \ncheck_connection - show connections of *all* or by tg id. \nadd_new_user *name*:*ip*:*tg* - add new user in database. \nremove_user *ip* - remove user from database by ip. \nanathem_user *** - eternal curse on user. \n mercy_user *tg* - mercy user from eternal curse.")

    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['time'])
def time(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        ips = get_my_ips(user_id)
        for ip in ips:
            new_message = str(ip) + " " + get_my_time(ip)
            bot.send_message(user_id, new_message, reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['status'])
def my_status(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        new_message = ""
        ips = get_my_ips(user_id)
        for ip in ips:
            status = get_my_status(ip)
            if str(status) == statuses.FlagBlocked:
                new_message = new_message + ip + " blocked.\n"
            elif str(status) == statuses.FlagNotBlocked:
                new_message = new_message + ip + " not blocked.\n"
            else:
                new_message = new_message + ip + " was anathemed. You did something really bad, contact your admininstrator or live with that curse.\n"
        bot.send_message(user_id, new_message, reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

@bot.message_handler(commands=['unblock'])
def unblock_me(message):
    user_id = message.from_user.id
    if  check_rights(user_id) == 1:
        result = module_unblock_user.by_tg(user_id)
        if result == 0:
            bot.send_message(user_id, "User unblocked successfully")
        else:
            bot.send_message(user_id, "User cannot be unblocked")
        #bot.send_message(user_id, new_message, reply_markup=markup)

#Answer for unknown command
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    if check_rights(user_id) == 0:
        bot.send_message(user_id, "Unknown command, buddy\nTry /help or something")
    elif check_rights(user_id) == 1:
        bot.send_message(user_id, "Unknown command, buddy\nTry /help or something", reply_markup=markup)
    else:
        bot.send_message(user_id, "Fuck off man, I have a job to do")

def check_users_time():
    import time
    while True:
        module_control_time.check_time()
        module_control_disturbers.control()
        time.sleep(600)

#Main function
#import time

#while True:
    #Add time to active users
#    module_control_time.check_time()
    #Block users that active too long
#    module_control_disturbers.control()
#    time.sleep(600)
from threading import Thread
th = Thread(target=check_users_time)
th.start()
bot.polling(none_stop=True, interval=0)
