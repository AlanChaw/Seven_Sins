echo "== Set variables =="
export node=115.146.92.10
export user=admin
export password=123456

echo "== Start the containers =="
docker run -d -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100:9100 couchdb:2.3.0
sleep 2

declare -a cont=`docker ps | grep couchdb | cut -f1 -d' '`

docker exec ${cont} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec ${cont} bash -c "echo \"-name couchdb@${node}\" >> /opt/couchdb/etc/vm.args"

docker restart ${cont[0]}
sleep 3

curl -X PUT "http://${node}:5984/_node/_local/_config/admins/${user}" --data "\"${password}\""
curl -X PUT "http://${user}:${password}@${node}:5984/_node/couchdb@${node}/_config/chttpd/bind_address" --data '"0.0.0.0"'
