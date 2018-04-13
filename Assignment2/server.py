#! /usr/bin/env python
import random

from mpi4py import MPI

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


# while True:
#     done = False
#     if rank == root:
#         message = comm.recv(source=0, tag=0)
#         if message is None:
#             done = True
#         else:
#             try:
#                 print('eval(%r) -> %r' % (message, eval(message)))
#             except Exception:
#                 print("invalid expression: %s" % message)
#     done = MPI.COMM_WORLD.bcast(done, root)
#     if done:
#         break

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
        rand_num = random.randint(1, M * 100)
        for client, data in index.items():  # for name, age in list.items():  (for Python 3.x)
            if rand_num in data:
                # send query to correct client
                comm.send(rand_num, dest=client, tag=0)
                # increase load by 1
                load[client] += 1


allocate_data()
search()

log('Server: disconnecting client...')
comm.Disconnect()

log('Server: unpublishing service...')
MPI.Unpublish_name(service, info, port)

log('Server: closing port...')
MPI.Close_port(port)
