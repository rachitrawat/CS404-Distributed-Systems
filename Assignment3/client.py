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
service = "server"
log("Client %s: looking-up service %s", rank, service)
port = MPI.Lookup_name(service)
log("Client %s: service located  at port %s", rank, port)

root = 0
log('Client %s: waiting for server connection...', rank)
comm = MPI.COMM_WORLD.Connect(port, info, root)
log('Client %s: server connected...', rank)

# timer value
T = 0


def initialize_timer():
    global T
    T = comm.recv(source=0, tag=0)
    log('Client %s has received timer value: %s', rank, T)
    log('Client %s has begun generating comments!', rank)


# generates random string of size 15
def rand_str_gen(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# write random strings in a file every T sec with probability 0.7
def write_comment_thread():
    threading.Timer(T, write_comment_thread).start()
    if random.randint(1, 100) <= 70:
        with open("client_comment/client" + str(rank) + ".txt", 'a+') as file_w:
            file_w.write(rand_str_gen() + " " + str(rank) + "\n")


# send commennts to server every T+10 sec
def send_server_thread():
    threading.Timer(T + 10, send_server_thread).start()
    with open("client_comment/client" + str(rank) + ".txt", 'r') as file_r:
        comment = file_r.read()
        comm.send(comment, dest=0, tag=0)
    # remove old comments after sending
    with open("client_comment/client" + str(rank) + ".txt", 'w') as file_w:
        pass


initialize_timer()

# start threads
write_comment_thread()
send_server_thread()
