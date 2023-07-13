import urllib.request as ureq
import nltk
import os
import tensorflow as tf
from tensorflow import keras
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import json
import pickle
import socket
stemmer = LancasterStemmer()
nltk.download('punkt')
ureq.urlretrieve('https://raw.githubusercontent.com/TXH2020/fast-labeling-workflow/master/abcd.json','intents.json')
# things we need for Tensorflow
with open('intents.json') as json_data:
    intents = json.load(json_data)
words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# remove duplicates
classes = sorted(list(set(classes)))

training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training=np.array(training,dtype=object)
# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])


model=keras.Sequential([
keras.layers.Dense(8,input_shape=(len(train_x[0]),),kernel_initializer='normal'),
keras.layers.Dense(8,kernel_initializer='normal'),
keras.layers.Dense(len(train_y[0]),activation='softmax',kernel_initializer='normal')])
model.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['accuracy'])
model.fit(np.array(train_x),np.array(train_y), epochs=1000, batch_size=8, verbose=1)
model.save('model.h5')

with open('intents.pkl','wb') as f:
  pickle.dump(intents,f)
with open('classes.pkl','wb') as f:
  pickle.dump(classes,f)
with open('words.pkl','wb') as f:
  pickle.dump(words,f)

a=1
b=1
c=''
with open('static/app.js','r') as f:
    s=f.read()
    a=s.find('https')
    b=s.find('predict')
    c=s[:a]
    c=c+"https://5000-"+socket.gethostname()+".ws-us81.gitpod.io/predict"+s[b+7:]
with open('static/app.js','w') as f:
    f.write(c)
