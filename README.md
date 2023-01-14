This project is a big data version of my AI Project(Main Repo--->Academics-->AI Project). The questions posed by users to the chatbot and the answers provided by the chatbot form the data. This data may hold some insights. But how do I fetch the data and store the data? At that time, I was fascinated by big data. My mind leaned towards using big data tools such as Apache Cassandra, Kafka and Spark. I built up an idea as follows:

<img src='IMG20230114203924.jpg'></img>

Basic idea is to stream data into a database and perform analysis to identify relevant questions and answers to be included in the intents.json I first started by first installing Apache Kafka on Windows, then installing an appropriate Java JDK and initializing the environment variables. After successfully starting Kafka on Windows, I could establish connection to Kafka topics through my Flask App(code present in repo) through Kafka-Python library. Since Kafka clusters maybe different nodes(computers) in a network, I thought of sending data to a Kafka cluster on my Virtual Machine. For this I had to change the hosts file on my computer to include the ip address and name of the VM for DNS resolution. Done.

The next step was to connect Kafka to a Cassandra database on my VM. I used DataStax Connector for this purpose. I followed the instructions given in the connector documentation. Done.



https://gitpod.io/#snapshot/a3cfedc0-4c15-472c-bce8-5c4cf79ea69f
