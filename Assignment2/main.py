from mpi4py import MPI

# initialize communicator
comm = MPI.COMM_WORLD

# returns the size of a communicator.
size = comm.Get_size()

# returns the rank of a process
rank = comm.Get_rank()

if rank == 0:
    msg = "Hello, world"
    comm.send(msg, dest=1)
elif rank == 1:
    s = comm.recv()
    print("rank %d: %s" % (rank, s))
