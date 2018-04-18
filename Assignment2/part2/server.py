#! /usr/bin/env python
import random
import matplotlib.pyplot as plt

from mpi4py import MPI
import numpy as np

M = int(input("\nEnter number of client nodes: "))

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    print()
    print(msg % args)


log('')

info = MPI.INFO_NULL

port = MPI.Open_port(info)
log("Server: opened port: '%s'", port)

service = 'search'
MPI.Publish_name(service, info, port)
log("Server: published service: '%s'", service)

# spawn client nodes
MPI.COMM_WORLD.Spawn("./client.py", maxprocs=M)

root = 0
log('Server: waiting for client connection...')
comm = MPI.COMM_WORLD.Accept(port, info, root)
log('Server: client connected...')

# index
index = {}
# load = number of queries pertaining to a given client node
load = {}


# allocate data to client nodes: 1-100,101-200.....
# set initial load to 0 for every client
def allocate_data():
    count = 0
    for i in range(0, M):
        data = list(range(count + 1, (count + 1) + 100))
        comm.send(data, dest=i, tag=0)
        index[i] = data
        load[i] = 0
        count += 100


# perform search
def search():
    for i in range(0, M):
        rand_num = np.random.zipf(2)
        for client, data in index.items():
            if rand_num in data:
                # send query to correct client
                log("Server: Sending query %s to client %s", rand_num, client)
                comm.send(rand_num, dest=client, tag=0)
                # increase load by 1
                load[client] += 1


# tell clients to print load and disconnect
def print_load():
    for i in range(0, M):
        comm.send("END", dest=i, tag=0)


allocate_data()
search()
print_load()

log('Server: disconnecting client...')
comm.Disconnect()

log('Server: unpublishing service...')
MPI.Unpublish_name(service, info, port)

log('Server: closing port...')
MPI.Close_port(port)

# plot node id vs load graph
plt.xlabel('Node ID', fontsize=16)
plt.ylabel('Load', fontsize=16)
plt.bar(list(load.keys()), load.values(), color='g')
plt.show()
