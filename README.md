# Heaven's door v0.7

telegram bot to control your VPN connection. Can be used for Wireguard VPN to control users, their online time and their connection.
Tired of people who use your VPN for too long? That bot will warn them first and block if they will go too far and unblock when they will earn your forgiveness .
## Intalling

Install the sqlite: ```sudo apt install sqlite3```

Install database: ```./setup.py```

Add Telegram API Token to config file .bot_token ```echo -n "TOKEN" > .bot_token```
## Using

```sudo ./new_bot.py```
## Admin commands
```
help - show all commands.
broadcast *message* - send message to all users. 
show_users - show all users table. 
show_time - show all users time table. 
show_configs - show all configs table. 
message *tg* *message* - send message to specified by tg user. 
block_user *tg* - block user if it's possible, check the status table. 
unblock_user *tg* - unblock user if it's possible, check the status table. 
check_connection - show connections of all or by tg id. 
add_new_user *name*:*ip*:*tg* - add new user in database. 
remove_user *ip* - remove user from database by ip
anathem_user *tg* - eternal curse on user.
mercy_user *tg* - mercy user from eternal curse.
```
## User commands
```
help - show all commands.
unblock - unblock user if it's possible.
time - show your active time.
status - show your status.
configs - show your configs.
```
