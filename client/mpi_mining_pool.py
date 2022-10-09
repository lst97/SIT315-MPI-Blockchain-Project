from multiprocessing import Process
import socket
import subprocess
from time import sleep
import requests
from datetime import datetime

NUMBER_OF_CLUSTER = "4"
def ping_listener():
    print(str(datetime.now()) + " [Pool] Listening PING...")
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 22061))
        s.listen()
        conn, addr = s.accept()
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            if data == "ping":
                print(str(datetime.now()) + " [Pool] PING received.")
                conn.sendall(b"pong")
        conn.close()

def main():
    p = Process(target=ping_listener)
    p.start()

    while(True):
        res = requests.get("http://localhost:8000/api/transections").json()
        if(len(res["message"]) == 0):
            print(str(datetime.now()) + " [Pool] Transections Pool is empty, slowing down...")
            sleep(3)
        else:
            print(str(datetime.now()) + " [Pool] Transections Detected, Mining START!")
            subprocess.call(['mpiexec', "-n", NUMBER_OF_CLUSTER, "python", "distribute.py"])
            print(str(datetime.now()) + " [Pool] Minded ONE block!")

if __name__ == '__main__':
    main()
