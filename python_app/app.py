from flask import Flask,render_template,request,jsonify
#from flask_cors import CORS
from kafka import KafkaProducer
from json import dumps
from kafka.admin import KafkaAdminClient, NewTopic
from cassandra.cluster import Cluster, NoHostAvailable
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError
from requests.exceptions import ConnectionError
import socket
import json
import requests
import logging
import time
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

admin_client = None
max_retries = 10
while max_retries > 0:
  try:
    admin_client = KafkaAdminClient(
        bootstrap_servers="broker:29092", 
        client_id='test'
    )
    break
  except NoBrokersAvailable:
    max_retries -= 1
    time.sleep(5)

if max_retries == 0:
  logger.error("Tried max_retries for establishing Kafka connection. Exiting")
  sys.exit(0)

topics = [NewTopic("ping", num_partitions=1, replication_factor=1)]

try:
  admin_client.create_topics(new_topics=topics)
except TopicAlreadyExistsError:
  logger.warning("Topic ping already exists")
  
admin_client.close()

# Create Cassandra keyspace and table
cluster = None
session = None

max_retries = 10
while max_retries > 0:
  try:
    cluster = Cluster([socket.gethostbyname('cassandra')])
    session = cluster.connect()
    break
  except NoHostAvailable:
    max_retries -= 1
    time.sleep(20)     

if max_retries == 0:
  logger.error("Tried max_retries for establishing Cassandra connection. Exiting")
  sys.exit(0)
  
session.execute("CREATE KEYSPACE if not exists ping_keyspace WITH replication = {'class': 'SimpleStrategy','replication_factor': 1};")
session.set_keyspace('ping_keyspace')
session.execute("CREATE TABLE if not exists ping_table (request text PRIMARY KEY, response text);")
cluster.shutdown()

# Send configuration file to Kafka Connect
config_json = json.load(open('connector-config.json','r'))
max_retries = 10

while max_retries > 0:
  try:
    requests.post('http://datastax-connect:8083/connectors', json=config_json)
    break
  except ConnectionError:
    max_retries -= 1
    time.sleep(10)

if max_retries == 0:
  logger.error("Tried max_retries for establishing Cassandra connector connection. Exiting")
  sys.exit(0)       

producer = KafkaProducer(bootstrap_servers = ["broker:29092"], value_serializer = lambda x : dumps(x).encode('utf-8'))

app = Flask(__name__)
#CORS(app)

@app.route('/',methods=['GET'])
def get():
    return(render_template('base.html'))

@app.route('/ping',methods=['POST'])
def ping():
    text = request.get_json().get('message')
    topic_data = {"request" : text, "response" : text}
    producer.send('ping', value=topic_data)
    producer.flush()
    message = {"answer" : text}
    return jsonify(message)
