#! /usr/bin/env python
import random

from mpi4py import MPI
import matplotlib.pyplot as plt

M = int(input("\nEnter number of client nodes: "))
T = int(input("\nEnter value of T seconds: "))

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    print()
    print(msg % args)


log('')

info = MPI.INFO_NULL

port = MPI.Open_port(info)
log("Server: opened port: '%s'", port)

service = 'master'
MPI.Publish_name(service, info, port)
log("Server: published service: '%s'", service)

# spawn client nodes
MPI.COMM_WORLD.Spawn("./client.py", maxprocs=M)

root = 0
log('Server: waiting for client connection...')
comm = MPI.COMM_WORLD.Accept(port, info, root)
log('Server: client connected...')


# allocate timer T to every client
def allocate_timer():
    for i in range(0, M):
        data = T
        comm.send(data, dest=i, tag=0)


allocate_timer()
