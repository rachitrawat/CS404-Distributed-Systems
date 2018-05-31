hadoop_dir=/usr/local/hadoop
target_dir=/app/hadoop/tmp
cd $hadoop_dir

# stop daemons and clean up
sbin/stop-yarn.sh
sbin/stop-dfs.sh
sudo rm -R /tmp/*
sudo rm -r $target_dir
sudo mkdir -p $target_dir
# sudo chown hduser:hadoop $target_dir
sudo chmod 750 $target_dir
