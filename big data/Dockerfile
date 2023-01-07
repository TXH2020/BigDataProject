FROM ubuntu:latest
RUN apt update
RUN apt install default-jdk -y
RUN apt install wget -y
RUN apt install net-tools -y
RUN wget https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz
RUN tar -xvf kafka_2.13-3.3.1.tgz
RUN wget https://dlcdn.apache.org/cassandra/4.1.0/apache-cassandra-4.1.0-bin.tar.gz
RUN tar -xvf apache-cassandra-4.1.0-bin.tar.gz
RUN wget https://downloads.datastax.com/kafka/kafka-connect-cassandra-sink-1.4.0.tar.gz
RUN tar -xvf kafka-connect-cassandra-sink-1.4.0.tar.gz
RUN rm kafka-connect-cassandra-sink-1.4.0.tar.gz
RUN rm kafka_2.13-3.3.1.tgz
RUN rm apache-cassandra-4.1.0-bin.tar.gz 
RUN rm kafka_2.13-3.3.1/config/connect-standalone.properties
COPY cassandra-sink.properties /kafka_2.13-3.3.1/config
COPY connect-standalone.properties /kafka_2.13-3.3.1/config
COPY database-setup.sh apache-cassandra-4.1.0
COPY setup.cql apache-cassandra-4.1.0
WORKDIR apache-cassandra-4.1.0
RUN ./database-setup.sh
RUN rm conf/cassandra.yaml
COPY cassandra.yaml conf
WORKDIR /
COPY startup_script.sh .
ENTRYPOINT ["./startup_script.sh"]

#To stop use docker stop container_name
