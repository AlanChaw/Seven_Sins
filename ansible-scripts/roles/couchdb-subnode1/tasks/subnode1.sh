#!/bin/bash

echo "== Set variables =="
export node=115.146.85.94
export user=admin
export password=123456

docker rm -f `docker ps -aq`

echo "== Start the containers =="
docker run -d -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100:9100 --name=subcouchdb1 couchdb:2.3.0
sleep 3

declare -a cont=`docker ps -aqf "name=subcouchdb1"`

docker exec ${cont} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec ${cont} bash -c "echo \"-name couchdb@${node}\" >> /opt/couchdb/etc/vm.args"

docker restart subcouchdb1
sleep 3
