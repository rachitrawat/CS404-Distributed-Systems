#! /usr/bin/env python
import random

from mpi4py import MPI
import numpy as np

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
# index
index = {}


# allocate data to client nodes: 1-100,101-200.....
def allocate_data():
    data = list(range((rank * 100) + 1, (rank + 1) * 100 + 1))
    index[rank] = data


# sync index across nodes
def sync_index():
    for i in range(0, size):
        data = comm.bcast(index, root=i)
        for k, v in data.items():
            if k not in index:
                index[k] = v


# generate M random queries & send to random nodes
def send_queries_randomly():
    for i in range(0, M):
        query = np.random.zipf(2)
        client = random.randint(0, size - 1)
        comm.send(query, dest=client, tag=0)
        log('Query %s randomly sent to client %s', query, client)


# output paths taken by query
def output_path():
    for i in range(0, M):
        query = comm.recv(source=0, tag=0)
        if query not in index[rank]:
            for client, data in index.items():
                if query in data:
                    # send query to correct client based on index
                    log("Client %s: Sending query %s to client %s", rank, query, client)
                    comm.send(query, dest=client, tag=0)
        else:
            log("Client %s: No need to redirect query %s", rank, query)


allocate_data()
sync_index()
if rank == 0:
    send_queries_randomly()
output_path()
