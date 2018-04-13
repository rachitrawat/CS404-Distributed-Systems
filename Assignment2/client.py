#! /usr/bin/env python

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    print(msg % args)


info = MPI.INFO_NULL
service = "pyeval"
log("Client %s: looking-up service %s", rank, service)
port = MPI.Lookup_name(service)
log("Client %s: service located  at port %s", rank, port)

root = 0
log('Client %s: waiting for server connection...', rank)
comm = MPI.COMM_WORLD.Connect(port, info, root)
log('Client %s: server connected...', rank)

# while True:
#     done = False
#     if rank == root:
#         try:
#             message = '1+1'
#             if message == 'quit':
#                 message = None
#                 done = True
#         except EOFError:
#             message = None
#             done = True
#         comm.send(message, dest=0, tag=0)
#     else:
#         message = None
#     done = MPI.COMM_WORLD.bcast(done, root)
#     if done:
#         break

comm.send("1+1", dest=0, tag=0)

log('Client %s: disconnecting server...', rank)
comm.Disconnect()
