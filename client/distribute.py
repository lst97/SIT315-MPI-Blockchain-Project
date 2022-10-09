# OpenCL for python is not possible for Apple Silicon, only Intel and Nvidia GPU

from datetime import datetime
from tkinter.messagebox import NO
from mpi4py import MPI
import requests
import random
import sys
import requests

sys.path.insert(1, '/Users/lst97/Documents/TODO/SIT315/M4T1D/backend/')
from database import DB
from utils import Hash

db = DB()
hash = Hash()

MASTER = 0
API_BASE_URL = "http://localhost:8000/api/"

def split(a, n):
    n = min(n, len(a))
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

comm = MPI.COMM_WORLD
world_comm = MPI.COMM_WORLD
world_size = world_comm.Get_size()
rank = world_comm.Get_rank()
chunk_size = world_size

if rank == MASTER:
    # get transections
    res = requests.get(API_BASE_URL + "transections")
    transections = res.json()['message']
    
    t_chunks = []
    idx = 0
    if (len(transections) >= chunk_size):
        t_chunks = list(split(transections, chunk_size))
    else:
        if(len(transections) != 0):
            t_chunks = list(split(transections, chunk_size))
            missing = chunk_size - len(t_chunks)
            for i in range(0, missing):
                t_chunks.append([])
        else:
            for i in range(0, chunk_size):
                t_chunks.append([])

    ################ Better doing this way.
    ###### Cluster should stop when a block is mined
    # # send to clusters
    # for i in range(0, len(t_chunks)):
    #     comm.send(t_chunks[i], dest=i+1)

    # #recive work
    # while(True):
    #     pending_block = comm.recv()
    #     print(pending_block)

else:
    t_chunks = None

# divided work
transections = comm.scatter(t_chunks, root=MASTER)

if (len(transections) != 0):
    data = ""
    for i in transections:
        data += i[1] + "#!"

    res = requests.get("http://localhost:8000/api/blocks/tail")
    prev_hash = res.json()["message"][2]

    nonce, valid_hash = hash.create_block_hash(data, prev_hash)
else:
    data = None
    valid_hash = None
    nonce = None

    if rank != MASTER:
        print(str(datetime.now()) + " [CLUSTER] No Block to be mine! TERMINATE")

pending_blocks = comm.gather([data, valid_hash, nonce],root=MASTER)

if rank == MASTER:
    while [None, None, None] in pending_blocks:
        pending_blocks.remove([None, None, None])

    if len(pending_blocks) != 0:
        block = pending_blocks[random.randint(0, len(pending_blocks) - 1)]

    db.insert_block(block[0], prev_hash, block[1], block[2])

MPI.Finalize()