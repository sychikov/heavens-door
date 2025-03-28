#!/bin/python3
from scripts import module_database
import wgconfig
import os


#Input should look like: "/remove_user *ip*"

#remove user from database
def remove_from_database(ip: str):
        try:
                dir = "/".join((os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
                cfg = wgconfig.WGConfig(dir + "/configs/wghub.conf")
                cfg.read_file()

                for peer_data in cfg.get_peers(False).values():
                        if ip in peer_data["AllowedIPs"]:
                                cfg.del_peer(peer_data["PublicKey"])
                                break

                cfg.write_file()

                module_database.change("delete from users where ip = \"" + ip + "\"")
                module_database.change("delete from time where ip = \"" + ip + "\"")
                module_database.change("delete from configs where ip = \"" + ip + "\"")
                return 0
        except Exception as e:
                print(e)
                return 1

#Main function
def remove(ip):
        if remove_from_database(ip) == 0:
                return 0
        else:
                return 1

if __name__ == "__main__":
        print(remove_from_database("<>"))
