## Cluster Configuration Manual Version

**以配置两台机器作为demo**

分别在主机`testInstance0(115.146.92.37)`和子机`testInstance2(115.146.92.10)`上各创建一个docker容器，需要将docker容器的`5984/5986/4369/9100`端口分别映射到宿主机的对应端口。

```bash
docker run -d -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100:9100 couchdb:2.3.0
```

之后获取该容器的ID，将cookie和nodename写入到对应的配置文件中，并重启动容器。

```bash
# testInstance0
docker ps

docker exec [ID] bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"

docker exec [ID] bash -c "echo \"-name couchdb@115.146.92.37\" >> /opt/couchdb/etc/vm.args"

docker restart [ID]

# testInstance2
docker ps

docker exec [ID] bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"

docker exec [ID] bash -c "echo \"-name couchdb@115.146.92.10\" >> /opt/couchdb/etc/vm.args"

docker restart [ID]
```

接下来操作在主机`testInstance0(115.146.92.37)`上完成。

```bash
curl -X PUT "http://115.146.92.37:5984/_node/_local/_config/admins/admin" --data "\"123456\""

curl -X PUT "http://admin:123456@115.146.92.37:5984/_node/couchdb@115.146.92.37/_config/chttpd/bind_address" --data '"0.0.0.0"'

curl -X PUT "http://115.146.92.10:5984/_node/_local/_config/admins/admin" --data "\"123456\""

curl -X PUT "http://admin:123456@115.146.92.10:5984/_node/couchdb@115.146.92.10/_config/chttpd/bind_address" --data '"0.0.0.0"'
```

将两个node添加到同一个cluster中

```bash
curl -X POST -H "Content-Type: application/json" http://admin:123456@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"123456", "port": 5984, "remote_node": "115.146.92.10", "remote_current_user": "admin", "remote_current_password": "123456" }'

curl -X POST -H "Content-Type: application/json" http://admin:123456@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"115.146.92.10", "port": "5984", "username": "admin", "password":"123456"}'

curl -X POST -H "Content-Type: application/json" http://admin:123456@127.0.0.1:5984/_cluster_setup -d '{"action": "finish_cluster"}'
```

删除nonode@nohost

```bash
rev=`curl -X GET "http://115.146.92.37:5986/_nodes/nonode@nohost" --user "admin:123456" | sed -e 's/[{}"]//g' | cut -f3 -d:`
curl -X DELETE "http://115.146.92.37:5986/_nodes/nonode@nohost?rev=${rev}"  --user "admin:123456"
```

至此cluster配置完毕。如果正确的话，应用下列命令可以看到cluster下所有的节点。

```bash
curl -X GET "http://admin:123456@115.146.92.10:5984/_membership"
# or
curl -X GET "http://admin:123456@115.146.92.37:5984/_membership"
```

输出

```json
{"all_nodes":["couchdb@115.146.92.10","couchdb@115.146.92.37"],"cluster_nodes":["couchdb@115.146.92.10","couchdb@115.146.92.37"]}
```

在任意一个节点上添加一个数据库，在两个节点上应该均能访问到该数据库。

```bash
curl -X PUT "http://admin:123456@115.146.92.10:5984/twitter"

curl -X GET "http://admin:123456@115.146.92.10:5984/_all_dbs"
# or
curl -X GET "http://admin:123456@115.146.92.37:5984/_all_dbs"
```

输出

```json
["_global_changes","_replicator","_users","twitter"]
```

