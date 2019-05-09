echo "== Set variables =="
declare -a nodes=(45.113.235.208, 103.6.254.24)
declare -a ports=(5984 5986 4369 9100)
export master_node=45.113.235.208
export master_port=5984
export size=${#nodes[@]}
export user=user
export pass=123456

echo "== Start the containers =="
docker run -d -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100:9100 couchdb:2.3.0
sleep 2

declare -a cont=`docker ps | grep couchdb | cut -f1 -d' '`

docker exec ${cont} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec ${cont} bash -c "echo \"-name couchdb@${master_node}\" >> /opt/couchdb/etc/vm.args"

docker restart ${cont}
sleep 3

echo "== Enable cluster setup =="
for (( i=0; i<${size}; i++ )); do
  curl -X POST "http://${user}:${pass}@localhost:${ports[${i}]}/_cluster_setup" -H 'Content-Type: application/json' \
    -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \"node_count\":\"${size}\"}"
done

echo "== Add nodes to cluster =="
for (( i=0; i<${size}; i++ )); do
  if [ "${nodes[${i}]}" != "${master_node}" ]; then
    curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@127.0.0.1:${master_port}/_cluster_setup \
      -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": 5984, \"node_count\": \"${size}\", \
           \"remote_node\": \"${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \"remote_current_password\": \"${pass}\"}"
    curl -X POST -H 'Content-Type: application/json' http://${user}:${pass}@127.0.0.1:${master_port}/_cluster_setup \
      -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": 5984, \"username\": \"${user}\", \"password\":\"${pass}\"}"
  fi
done

curl -X POST "http://${user}:${pass}@localhost:${master_port}/_cluster_setup" -H 'Content-Type: application/json' -d '{"action": "finish_cluster"}'

curl http://${user}:${pass}@localhost:${master_port}/_cluster_setup

echo "== Allow cross-domain access =="
curl -X PUT http://${user}:${pass}@127.0.0.1:5984/_node/couchdb@127.0.0.1:5984/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://${user}:${pass}@127.0.0.1:5984/_node/couchdb@127.0.0.1:5984/_config/cors/origins -d '"*"'
curl -X PUT http://${user}:${pass}@127.0.0.1:5984/_node/couchdb@127.0.0.1:5984/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'

for port in "${ports[@]}"; do  curl -X GET http://${user}:${pass}@localhost:${port}/_membership; done
