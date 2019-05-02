echo "== Set variables =="
declare -a nodes=(115.146.92.37 115.146.92.10)
declare -a ports=(5984 5986 4369 9100)
export master_node=115.146.92.37
export master_port=5984
export size=${#nodes[@]}
export user=user
export pass=123456

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
