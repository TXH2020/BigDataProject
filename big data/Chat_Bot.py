#This file is the model updater. It updates the model each time a new intents.json is uploaded. Basically we use the concept of online machine learning where we do not train 
#on new instances from scratch every time but only on the new data. Similarly, we append new instances to the words, classes and intents data structures and pickle them but
#not recompute them from scratch.

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
stemmer = LancasterStemmer()
nltk.download('punkt')
ureq.urlretrieve('https://raw.githubusercontent.com/TXH2020/MainRepo/main/Academics/AI%20Project/intents.json','intents.json')
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
training = np.array(training)

# create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

model=None
if(os.path.isfile('model.h5')==False):
    model=keras.Sequential([
    keras.layers.Dense(8,input_shape=(len(train_x[0]),),kernel_initializer='normal'),
    keras.layers.Dense(8,kernel_initializer='normal'),
    keras.layers.Dense(len(train_y[0]),activation='softmax',kernel_initializer='normal')])
    model.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['accuracy'])
else:
    model = tf.keras.models.load_model('model.h5')
model.fit(np.array(train_x),np.array(train_y), epochs=1000, batch_size=8, verbose=1)
model.save('model.h5')

def check_file(name,file):
 if(os.path.isfile(name)==False):
  with open(name,'wb') as f:
  	pickle.dump(file,f)
 else:
  with open(name,'rb') as f:
	new_file=pickle.load(f)
  if(type(file)==dict):
   new_file['intents'].extend(file['intents'])
  else:
   new_file.extend(file)
  with open(name,'wb') as f:
	pickle.dump(new_file,f)

check_file('intents.pkl',intents)
check_file('classes.pkl',classes)
check_file('words.pkl',words)
