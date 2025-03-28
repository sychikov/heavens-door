# Heaven's door v1.3

Telegram bot to control your VPN connection. Can be used for Wireguard VPN to control users, their online time and their connection.
Tired of people who use your VPN for too long? That bot will warn them first and block if they will go too far and unblock when they will earn your forgiveness. You can create new configs without connect to server by yourself.
## Intalling

Install sqlite: ```sudo apt install sqlite3```

Install Wireguard: ```sudo apt install wireguard```

Install requirements: ```pip3 install -r requirements.txt```

Install database and Wireguard server: ```./setup.py```

Add Telegram API Token to config file .bot_token ```echo -n "TOKEN" > .bot_token```
## Using

```sudo ./new_bot.py```
## Admin commands
```
/help - show all commands. 

Get info: 

/show_users - show all users table. 
/show_time - show all users time table. 
/show_configs - show all configs table. 
/get_configs *tg* - get all configs associated with tg id. 
/check_connection - show connections of *all* or by tg id. 

Contact with users: 

/broadcast *message* - send message to all users in database. 
/message *tg* *message* - send message to specified by tg user. 

Control user's activity: 

/easy_add *name*:*tg* - add user by easy way with only name and telegram id. 
/block_user *tg* - block user if it's possible, check the status table. 
/remove_peer *ip* - remove peer from database by ip. 
/anathem_user *tg* - eternal curse on user. 
/mercy_user *tg* - mercy/unblock user and update database.. 

Wireguard commands: 

/get_server_config - get server config file. 
```
## User commands
```
/help - show all commands.
/unblock - unblock user if it's possible.
/time - show your active time.
/status - show your status.
/configs - show your configs.
```
