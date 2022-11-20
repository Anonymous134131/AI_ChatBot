import json
import pickle
import random 
import numpy as np 
import tensorflow as tf
import tflearn
import nltk
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from nltk.stem.lancaster import LancasterStemmer 

stemmer = LancasterStemmer()

with open("../src/intent.json") as file:
    intents = json.load(file)
lang = "en"
nltk.download('punkt') # This will download a text based data set straight into the notebook file

class train_model:
    def __init__(self):
        self.words = []
        self.classes = []
        self.tags = []
        self.ignore_words =['?']
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.tags.append((w, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))

        # remove duplicates
        self.classes = sorted(list(set(self.classes)))

        print (len(self.tags), "tags")
        print (len(self.classes), "classes", self.classes)
        print (len(self.words), "unique stemmed words", self.words)

        training = []
        output = []
        output_empty = [0] * len(self.classes)

        for tag in self.tags:

            bag = []
            pattern_words = tag[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[self.classes.index(tag[1])] = 1

            training.append([bag, output_row])


        random.shuffle(training)
        training = np.array(training)

        # create train and test lists
        self.train_x = list(training[:,0])
        self.train_y = list(training[:,1])

        # reset underlying graph data
        tf.compat.v1.reset_default_graph()

        #Building the Neural Network
        net = tflearn.input_data(shape=[None, len(self.train_x[0])])
        net = tflearn.fully_connected(net, 10)
        net = tflearn.fully_connected(net, 10)
        net = tflearn.fully_connected(net, len(self.train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        # Start training (apply gradient descent algorithm)
        self.model.fit(self.train_x, self.train_y, n_epoch=1000, batch_size=8, show_metric=True)
        self.model.save('model.tflearn')

        pickle.dump( {'words':self.words, 'classes':self.classes, 'train_x':self.train_x, 'train_y':self.train_y}, open( "training_data", "wb" ) )

        data = pickle.load( open( "training_data", "rb" ) )
        self.words = data['words']
        self.classes = data['classes']
        self.train_x = data['train_x']
        self.train_y = data['train_y']
        self.ERROR_THRESHOLD = 0.2



   