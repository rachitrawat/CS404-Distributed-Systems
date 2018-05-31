# set up dir
hadoop_dir=/usr/local/hadoop
hdfs=bin/hdfs
src_dir=/home/su/Desktop/hadoop
cd $hadoop_dir
rm -r output
rm -r $src_dir/output/

# format the filesystem
$hdfs namenode -format

# start NameNode daemon and DataNode daemon
sbin/start-dfs.sh

# namenode - Safe mode off
$hdfs dfsadmin -safemode leave

# open namenode web interface
xdg-open http://localhost:9870/

# make the HDFS directories required to execute MapReduce jobs
$hdfs dfs -mkdir /user
$hdfs dfs -mkdir /user/su

# Start ResourceManager daemon and NodeManager daemon
sbin/start-yarn.sh

# open ResourceManager web interface
xdg-open http://localhost:8088/

# copy the input files into the distributed filesystem
$hdfs dfs -mkdir input
$hdfs dfs -put $src_dir/input/* input
cp $src_dir/program/WordCount.java WordCount.java

# compile WordCount.java and create a jar
bin/hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class

# run the application
bin/hadoop jar wc.jar WordCount input output

# copy the output files from the distributed filesystem to the local filesystem
$hdfs dfs -get output output
cp -a output/. $src_dir/output/
