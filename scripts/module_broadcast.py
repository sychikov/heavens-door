#!/bin/python3
from scripts import module_database

#Get telegram ids of all clients
def get_all_tgs():
        tgs = module_database.get("select tg from users")
        tgs = tgs.split("\n")
        return tgs

#Delete similar tg ids
def delete_same(clients):
        clients_clean = ['']
        for client in clients:
                #print(client)
                if not client in clients_clean:
                        clients_clean.append(client)
        return clients_clean

#Get list of clients to send broadcast message
def get_clients():
        clients = get_all_tgs()
        #print(clients)
        if clients:
                return delete_same(clients)
