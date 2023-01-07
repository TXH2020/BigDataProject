#!/bin/bash

apache-cassandra-4.1.0/bin/cassandra -R
sleep 20
kafka_2.13-3.3.1/bin/zookeeper-server-start.sh -daemon kafka_2.13-3.3.1/config/zookeeper.properties
sleep 20
kafka_2.13-3.3.1/bin/kafka-server-start.sh -daemon kafka_2.13-3.3.1/config/server.properties
sleep 40
kafka_2.13-3.3.1/bin/connect-standalone.sh kafka_2.13-3.3.1/config/connect-standalone.properties kafka_2.13-3.3.1/config/cassandra-sink.properties
