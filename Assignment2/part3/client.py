#! /usr/bin/env python

from mpi4py import MPI

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
#
# while (True):
#     query = comm.recv(source=0, tag=0)
#     if query == "END":
#         log("Load at client %s is %s", rank, load[rank])
#         break
#     else:
#         log("Client %s: Received query %s from server", rank, query)
#         load[rank] += 1
#
# log('Client %s: disconnecting server...', rank)
# comm.Disconnect()
