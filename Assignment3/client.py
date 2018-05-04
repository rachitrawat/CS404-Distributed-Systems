#! /usr/bin/env python
import random
import string
import threading

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    print()
    print(msg % args)


info = MPI.INFO_NULL
service = "master"
log("Client %s: looking-up service %s", rank, service)
port = MPI.Lookup_name(service)
log("Client %s: service located  at port %s", rank, port)

root = 0
log('Client %s: waiting for server connection...', rank)
comm = MPI.COMM_WORLD.Connect(port, info, root)
log('Client %s: server connected...', rank)

# data of each client
data = []
T = 0


def initialize_timer():
    global T
    T = comm.recv(source=0, tag=0)
    log('Client %s has received timer value: %s...', rank, T)


def comment_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def run_thread():
    threading.Timer(T, run_thread).start()
    if random.randint(1, 100) <= 70:
        with open(str(rank) + ".txt", 'a+') as file:
            file.write(comment_generator() + " " + str(rank) + "\n")


initialize_timer()
if rank == 0:
    print("Writing comments every %s seconds with probability 0.7" % T)
run_thread()
