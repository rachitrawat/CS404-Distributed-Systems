# hadoop Pseudo-distributed mode
scripts to start hadoop in pseudo-distributed mode

Pseudo Distributed Mode(Single Node Cluster)
Configuration is required in given 3 files for this mode
Replication factory is one for HDFS.
Here one node will be used as Master Node / Data Node / Job Tracker / Task Tracker
Used for Real Code to test in HDFS.
Pseudo distributed cluster is a cluster where all daemons are
running on one node itself.

input: text documents in increasing order of size (file1<file2<file3)

output: <word> <frequency> pair [stop words removed]

program: code in Java and Python used to run MapReduce jobs

graph: Visualizations of output [Visualize.py used to generate graphs]

start.sh: script used to start hadoop daemons

stop.sh: script used to stop hadoop daemons 
