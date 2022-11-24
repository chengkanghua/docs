#!/bin/sh
# docker-compose启动mongodb分片容器组服务
docker-compose -f mongo-compose.yaml up -d

# 睡眠半分钟，等待mongodb所有容器起来之后将它们配置加入分片
sleep 30s

# 操作config1，配置config副本集，将config容器组作为config角色,此时config1作为config副本集里的主节点
docker-compose -f mongo-compose.yaml exec config1 bash -c "echo 'rs.initiate({_id: \"mongo-config\",configsvr: true, members: [{ _id : 0, host : \"config1:27019\" },{ _id : 1, host : \"config2:27019\" }, { _id : 2, host : \"config3:27019\" }]})' | mongo --port 27019"

# 操作shard1、shard2、shard3，将shard容器组作为shard角色。
docker-compose -f mongo-compose.yaml exec shard1 bash -c "echo 'rs.initiate({_id: \"shard1\",members: [{ _id : 0, host : \"shard1:27018\" }]})' | mongo --port 27018"
docker-compose -f mongo-compose.yaml exec shard2 bash -c "echo 'rs.initiate({_id: \"shard2\",members: [{ _id : 0, host : \"shard2:27018\" }]})' | mongo --port 27018"
docker-compose -f mongo-compose.yaml exec shard3 bash -c "echo 'rs.initiate({_id: \"shard3\",members: [{ _id : 0, host : \"shard3:27018\" }]})' | mongo --port 27018"

# 将shard1、shard2、shard3加入分片集群组。
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard1/shard1:27018\")' | mongo"
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard2/shard2:27018\")' | mongo"
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard3/shard3:27018\")' | mongo"