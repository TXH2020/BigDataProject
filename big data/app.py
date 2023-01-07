#This file is responsible for the frontend. It also uses Kafka Client to send topics containing user questions and responses to those questions to 
#the Kafka server running on the Virtual Machine with IP 192.168.0.203

from flask import Flask,render_template,request,jsonify
from chat import response
from flask_cors import CORS
from kafka import KafkaProducer
from json import dumps
import logging
logging.basicConfig(level=logging.DEBUG)
producer = KafkaProducer(bootstrap_servers=["localhost"],value_serializer = lambda x:dumps(x).encode('utf-8'))
app = Flask(__name__)
CORS(app)
@app.route('/',methods=['GET','POST'])
def get():
    return(render_template('base.html'))
@app.route('/predict',methods=['GET','POST'])
def predict():
    text=request.get_json().get('message')
    user_response=response(text)
    topic_data={"question":text,"answer":user_response}
    producer.send('chat_topic1', value=topic_data)
    producer.flush()
    message={"answer":user_response}
    return jsonify(message)
