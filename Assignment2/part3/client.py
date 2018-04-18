#! /usr/bin/env python
import random

from mpi4py import MPI

# number of queries
M = 10

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
# total no of processes
size = comm.Get_size()


def log(msg, *args):
    print()
    print(msg % args)


# data of each client
data = []
# load = number of queries pertaining to a given client node
load = {}
# index
index = {}


# allocate data to client nodes: 1-100,101-200.....
# set initial load to 0 for every client
def allocate_data():
    data = list(range((rank * 100) + 1, (rank + 1) * 100 + 1))
    index[rank] = data
    load[rank] = 0


# sync index across nodes
def sync_index():
    for i in range(0, size):
        data = comm.bcast(index, root=i)
        for k, v in data.items():
            if k not in index:
                index[k] = v


allocate_data()
sync_index()

if rank == 0:
    for i in range(0, M):
        # generate random query & send to random nodes
        query = random.randint(1, (size + 1) * 100)
        comm.send(query, dest=random.randint(0, size - 1), tag=0)

while (True):
    query = comm.recv(source=0, tag=0)
    log('Client %s: received query %s', rank, query)
    # if query not with client
    if query not in index[rank]:
        for client, data in index.items():
            if query in data:
                # send query to correct client based on index
                log("Client %s: Sending query %s to client %s", rank, query, client)
                comm.send(query, dest=client, tag=0)

# log('Client %s: disconnecting server...', rank)
# comm.Disconnect()