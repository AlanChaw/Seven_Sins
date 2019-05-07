#!/bin/bash

echo "== Set variables =="
declare -a nodes=(103.6.254.104 103.6.254.117)
export masternode=103.6.254.104
export size=${#nodes[@]}
export user=admin
export password=123456

echo "== Start the container =="
docker run -d -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100:9100 --name=mastercouchdb couchdb:2.3.0
sleep 3

# declare -a cont=`docker ps | grep couchdb | cut -f1 -d' '`
declare -a cont=`docker ps -aqf "name=mastercouchdb"`

docker exec ${cont} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec ${cont} bash -c "echo \"-name couchdb@${masternode}\" >> /opt/couchdb/etc/vm.args"

docker restart mastercouchdb
sleep 3

echo "== Enable cluster setup =="

# curl -X PUT "http://${masternode}:5984/_node/_local/_config/admins/${user}" --data "\"${password}\""
# curl -X PUT "http://${user}:${password}@${masternode}:5984/_node/couchdb@${masternode}/_config/chttpd/bind_address" --data '"0.0.0.0"'

# for (( i=0; i<${size}; i++ )); do
#     if [ "${nodes[${i}]}" != "${masternode}" ]; then
#         curl -X PUT "http://${nodes[${i}]}:5984/_node/_local/_config/admins/${user}" --data "\"${password}\""
#         curl -X PUT "http://${user}:${password}@${nodes[${i}]}:5984/_node/couchdb@${nodes[${i}]}/_config/chttpd/bind_address" --data '"0.0.0.0"'
#     fi
# done

for (( i=0; i<${size}; i++ )); do
    curl -X PUT "http://${nodes[${i}]}:5984/_node/_local/_config/admins/${user}" --data "\"${password}\""
    curl -X PUT "http://${user}:${password}@${nodes[${i}]}:5984/_node/couchdb@${nodes[${i}]}/_config/chttpd/bind_address" --data '"0.0.0.0"'
done

echo "== Add nodes to cluster =="
for (( i=0; i<${size}; i++ )); do
    echo "${nodes[${i}]}"
    if [ "${nodes[${i}]}" != "${masternode}" ]; then
        curl -X POST -H 'Content-Type: application/json' http://${user}:${password}@${masternode}:5984/_cluster_setup \
            -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${password}\", \"port\": 5984, \"node_count\": \"${size}\", \
            \"remote_node\": \"${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \"remote_current_password\": \"${password}\"}"
        curl -X POST -H 'Content-Type: application/json' http://${user}:${password}@${masternode}:5984/_cluster_setup \
            -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": 5984, \"username\": \"${user}\", \"password\":\"${password}\"}"
    fi
done

echo "== Finish cluster =="
curl -X POST -H "Content-Type: application/json" "http://${user}:${password}@${masternode}:5984/_cluster_setup" -d '{"action": "finish_cluster"}'

# rev=`curl -X GET "http://${masternode}:5986/_nodes/nonode@nohost" --user "${user}:${password}" | sed -e 's/[{}"]//g' | cut -f3 -d:`
# curl -X DELETE "http://${masternode}:5986/_nodes/nonode@nohost?rev=${rev}"  --user "${user}:${password}"
