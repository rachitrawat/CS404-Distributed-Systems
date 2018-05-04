#! /usr/bin/env python

import threading

from mpi4py import MPI

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

service = 'server'
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
        comm.send(T, dest=i, tag=0)


# recv comments from client every T+10 sec
def recv_comment_thread():
    threading.Timer(T + 10, recv_comment_thread).start()
    with open("server_comment/server.txt", 'a+') as file_w:
        for i in range(0, M):
            comment = comm.recv(source=i, tag=0)
            file_w.write(comment)


allocate_timer()

# start thread
recv_comment_thread()
