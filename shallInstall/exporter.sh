wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
tar xvfz node_exporter-1.2.2.linux-amd64.tar.gz 
mv node_exporter-1.2.2.linux-amd64   /usr/local/node_exporter-1.2.2.linux-amd64
cd /usr/local/node_exporter-1.2.2.linux-amd64
nohup ./node_exporter>node.logs 2>&1 &