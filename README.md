# Big Data Project
This example shows how to ingest JSON records from [Kafka](https://kafka.apache.org/) to multiple tables in the [Cassandra](https://cassandra.apache.org/) database using the [DataStax Apache Kafka Connector](https://docs.datastax.com/en/kafka/doc/index.html).

## Project Layout
- [Dockerfile-connector](Dockerfile-connector): Dockerfile to build an image of Kafka Connect with the DataStax Kafka Connector installed.
- [Dockerfile-producer](python_app/Dockerfile): Dockerfile to build an image for the producer contained in this repository.
- [docker-compose.yml](docker-compose.yml): Uses Kafka and Cassandra docker images to set up Kafka Brokers, Kafka Connect, Apache Cassandra, and the producer container.
- [connector-config.json](python_app/connector-config.json): Configuration file for the DataStax Kafka Connector to be used with the distributed Kafka Connect Worker.
- [producer](python_app/): Contains the Kafka Python Producer to write records to Kafka.

## How this works
After running the docker and docker-compose commands, there will be 4 docker containers running, all using the same docker network.

After writing records to the Kafka Brokers, the DataStax Kafka Connector will be started which will start the stream of records from Kafka to the Cassandra database, writing a single record to a table in the database.

## Setup & Running
### Prerequisites
- Docker

### Setup
Clone this repository
```
git clone https://github.com/DataStax-Examples/kafka-connector-sink-json.git
```

Go to the directory
```
cd BigDataProject
```

Open python_app/static/app.js. There is a comment saying "Fix IP...". If we put localhost, it requires the browser to be opened within the same computer where the containers are run. Setting an IP/hostname allows external clients to access the service.

Start Kafka Brokers, Kafka Connect, Cassandra, and the producer containers
```
docker-compose up -d
```

### Running
After building the images, it takes about 5 min for the service to be ready. To check if the service is ready or not, open a browser and goto <IP>:5000. You should see a chat button at the bottom. The chatbot is simply a ping pong bot, which returns whatever you type in. Unique strings that you type in will appear in the cassandra table. This is just to demonstrate an interesting end to end flow. 

#### Confirm rows written to Cassandra
Start a cqlsh shell on the Cassandra node
```
docker exec -it cassandra cqlsh
```

Confirm rows were written to each of the Cassandra tables
```
select * from ping_keyspace.ping_table;
```
```

 request | response
---------+----------
      hi |       hi

(1 rows)

```
```
select * from kafka_examples.stocks_table_by_exchange limit 10;
```
```

 request | response
---------+----------
   hello |    hello
      hi |       hi

(2 rows)

```

## Bonus: Connect Spark to Cassandra

1. Install Python. Create a Virtual Environment
2. pip install pyspark
3. pyspark --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1 --conf spark.cassandra.connection.host=172.18.0.3 --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions.
   
   Find the IP of the Cassandra container using docker inspect and pass it as shown above.
4. Type in the following commands in pyspark shell:
   1. spark.conf.set("spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")
   2. spark.read.table("myCatalog.ping_keyspace.ping_table").show()