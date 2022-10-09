import sqlite3
from utils import Hash

DB_PATH = "/Users/lst97/Documents/TODO/SIT315/M4T1D/backend/db.sqlite"
hash = Hash()

class Server:
    API = 0
    DATABASE = 1
    MINING_POOL = 2
    CLUSTERS = 3

class Status:
    OFFLINE = "offline"
    ONLINE = "online"


class DB:
    def __init__(self) -> None:
        conn = sqlite3.connect(DB_PATH)
        conn.close()

    @staticmethod
    def insert_block(data:str, prev_hash, block_hash, nonce):
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()
        
        # checkvalid block
        new_nonce, new_block_hash = hash.create_block_hash(data, prev_hash, nonce, nonce + 1)
        if nonce == new_nonce and block_hash == new_block_hash:
            cursor.execute(
                """INSERT INTO BLOCKS (DATA, HASH, PREV_HASH, NONCE) VALUES(?, ?, ?, ?);""",(data, block_hash, prev_hash, nonce,)
            )
        
        # remove transection from tran pool
        mined_transections = data.split("#!")[:-1]
        for transection in mined_transections:
            res = cursor.execute("""SELECT * FROM TRANSECTIONS WHERE DATA = ?""",(transection,))
            tran_id = res.fetchall()[0][0]
            cursor.execute("""DELETE FROM TRANSECTIONS WHERE DATA = ? AND ID = ?""",(transection, tran_id))

        conn.commit()
        conn.close()


    @staticmethod
    def update_server_status(server:Server, ip:str, port:int, status:str):
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()
        
        if server == Server.API:

            res = cursor.execute("""SELECT NAME FROM SERVER_STATUS WHERE NAME = ?""", ('API',))
            if len(res.fetchall()) == 0:
                cursor.execute(
                    """INSERT INTO SERVER_STATUS (NAME, IP, PORT, STATUS) VALUES(?, ?, ?, ?);""",('API', ip, port, status,)
                )

            cursor.execute(
                """UPDATE SERVER_STATUS SET STATUS = ? WHERE NAME = 'API';""",(status,)
            )
        if server == Server.MINING_POOL:
            res = cursor.execute("""SELECT NAME FROM SERVER_STATUS WHERE NAME = ?""", ('MINING_POOL',))
            if len(res.fetchall()) == 0:
                cursor.execute(
                    """INSERT INTO SERVER_STATUS (NAME, IP, PORT, STATUS) VALUES(?, ?, ?, ?);""",('MINING_POOL', ip, port, status,)
                )

            cursor.execute(
                """UPDATE SERVER_STATUS SET STATUS = ? WHERE NAME = 'MINING_POOL';""",(status,)
            )
        conn.commit()
        conn.close()

    @staticmethod
    def fetch_server_status():
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()

        result = cursor.execute("""SELECT * FROM SERVER_STATUS;""").fetchall()
        conn.close()
        #[[1, "API", "127.0.0.1", "8000", "online"]]

        return result

    @staticmethod
    def fetch_blocks():
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()

        result = cursor.execute("""SELECT * FROM BLOCKS;""").fetchall()
        conn.close()
        return result

    
    def init(self):
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()
        # Blocks
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS BLOCKS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
            DATA           TEXT     NOT NULL,
            HASH           TEXT     NOT NULL,
            PREV_HASH      TEXT     NOT NULL,
            NONCE          INTEGER      NOT NULL);"""
        )

        # create root block
        # .execute("SELECT weight FROM Equipment WHERE name = ?", [item])
        data = 'INITIAL_BLOCK'
        nonce, valid_hash = hash.create_block_hash(data)
        print("[SQLite3] Mining Initial Block...")
        print("[SQLite3] DONE - {" + data + "," + valid_hash + "," + str(nonce) + "}")
        
        results = cursor.execute("""SELECT HASH FROM BLOCKS WHERE HASH = ?""", (valid_hash,))
        if(results.fetchone() is None):
            cursor.execute(
                """INSERT INTO BLOCKS (DATA, HASH, PREV_HASH, NONCE) VALUES(?, ?, ?, ?);""",(data, valid_hash, "", nonce,)
            )

        # Transection waiting to be add into block
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS TRANSECTIONS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
            DATA           TEXT     NOT NULL);"""
        )
        
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS SERVER_STATUS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
            NAME         TEXT       NOT NULL,
            IP           TEXT       NOT NULL,
            PORT         TEXT       NOT NULL,
            STATUS       INTEGER        NOT NULL);"""
        )

        conn.commit()
        conn.close()
        print("[SQLite3] Initial DONE.")

    @staticmethod
    def insert_transection(data:str):
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()

        cursor.execute(
            """INSERT INTO TRANSECTIONS (DATA) VALUES(?);""", (str(data),)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def fetch_transections():
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()

        result = cursor.execute("""SELECT * FROM TRANSECTIONS;""").fetchall()

        conn.commit()
        conn.close()

        return result

    @staticmethod
    def fetch_last_block():
        conn = sqlite3.connect(DB_PATH)
        cursor=conn.cursor()

        result = cursor.execute("""SELECT * FROM BLOCKS;""").fetchall()

        conn.commit()
        conn.close()

        return result[-1]
