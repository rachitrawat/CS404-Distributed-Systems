#! /usr/bin/env python

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    if rank == 0:
        print(msg % args)


info = MPI.INFO_NULL
service = "pyeval"
log("Client: looking-up service '%s'", service)
port = MPI.Lookup_name(service)
log("Client: service located  at port '%s'", port)

root = 0
log('Client: waiting for server connection...')
comm = MPI.COMM_WORLD.Connect(port, info, root)
log('Client: server connected...')

while True:
    done = False
    if rank == root:
        try:
            message = input('pyeval>>> ')
            if message == 'quit':
                message = None
                done = True
        except EOFError:
            message = None
            done = True
        comm.send(message, dest=0, tag=0)
    else:
        message = None
    done = MPI.COMM_WORLD.bcast(done, root)
    if done:
        break

log('Client: disconnecting server...')
comm.Disconnect()
