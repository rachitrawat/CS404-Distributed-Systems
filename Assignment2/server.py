#! /usr/bin/env python

from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()


def log(msg, *args):
    print(msg % args)


log('')

info = MPI.INFO_NULL

port = MPI.Open_port(info)
log("Server: opened port: '%s'", port)

service = 'pyeval'
MPI.Publish_name(service, info, port)
log("Server: published service: '%s'", service)

MPI.COMM_WORLD.Spawn("./client.py", maxprocs=5)

root = 1
log('Server: waiting for client connection...')
comm = MPI.COMM_WORLD.Accept(port, info, root)
log('Server: client connected...')

while True:
    done = False
    if rank == root:
        message = comm.recv(source=0, tag=0)
        if message is None:
            done = True
        else:
            try:
                print('eval(%r) -> %r' % (message, eval(message)))
            except Exception:
                print("invalid expression: %s" % message)
    done = MPI.COMM_WORLD.bcast(done, root)
    if done:
        break

log('Server: disconnecting client...')
comm.Disconnect()

log('Server: unpublishing service...')
MPI.Unpublish_name(service, info, port)

log('Server: closing port...')
MPI.Close_port(port)
