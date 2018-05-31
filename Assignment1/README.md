# hadoop Pseudo-distributed mode
scripts to start hadoop in pseudo-distributed mode

The Hadoop daemons run on a local machine, thus simulating a cluster on a small scale. Different Hadoop daemons run in different JVM instances, but on a single machine. HDFS is used instead of local FS.

input: text documents in increasing order of size (file1<file2<file3)

output: <word> <frequency> pair [stop words removed]

program: code in Java and Python used to run MapReduce jobs

graph: Visualizations of output [Visualize.py used to generate graphs]

start.sh: script used to start hadoop daemons

stop.sh: script used to stop hadoop daemons 
