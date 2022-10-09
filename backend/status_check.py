# server for check other server status.
from time import sleep
import requests
from database import DB
from database import Status
from database import Server
from datetime import datetime
import socket

class Checker:
    def __init__(self, repeat_time:int = 15) -> None:
        # second
        self.repeat_time = repeat_time

    def start(self):
        db = DB()
        while(True):
            print(str(datetime.now()) + " [STATUS CHECKER] Checking Server Status...")
            res = requests.get("http://127.0.0.1:8000/api/ping")
            if res.status_code == 200:
                print(str(datetime.now()) + " [STATUS CHECKER] API - ONLINE")
                # update API server status
                db.update_server_status(Server.API, '127.0.0.1', 8000, Status.ONLINE)
            else:
                print(str(datetime.now()) + " [STATUS CHECKER] API - OFFLINE")
                db.update_server_status(Server.API, '127.0.0.1', 8000, Status.OFFLINE)

            # Mining Pool
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(('localhost', 22061))
                s.sendall(b'ping')
                data = s.recv(1024)
                s.close()
            except socket.error as e:
                db.update_server_status(Server.MINING_POOL, "127.0.0.1", "22061", "offline")
                print(str(datetime.now()) + " [STATUS CHECKER] Pool - OFFLINE")
                sleep(self.repeat_time)
                continue

            if(data.decode('utf-8') == "pong"):
                db.update_server_status(Server.MINING_POOL, "127.0.0.1", "22061", "online")
                print(str(datetime.now()) + " [STATUS CHECKER] Pool - ONLINE")

            sleep(self.repeat_time)
Checker(5).start()