from queue import Empty
import speech_recognition as s
import pyttsx3 
import datetime

texttospeech = pyttsx3.init('sapi5')
texttospeech.setProperty('voice', texttospeech.getProperty('voices')[1].id)
import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("../src/intent.json") as file:
    data = json.load(file)

def speak(text):
    texttospeech.say(text)
    texttospeech.runAndWait()

def takeCommand():
    recognizer= s.Recognizer()
    microphone = s.Microphone()
    
    with microphone as source:
        print("Listening....")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
     print("Recognizing....")
     query = recognizer.recognize_google(audio, language='en-in')
     print(f"user said: {query}\n")
    except Exception as e:
      print(e)
      return "None"
    return query

if __name__=='__main__':
     # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    hour=datetime.datetime.now().hour
    if hour>0 and hour<12:
        speak("Hello, Good Morning,")
        speak("Tell me how can I help you now?")
        print('Hello, Good Morning')
        print("Tell me how can I help you now?")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        speak("Tell me how can I help you now?")
        print("Hello,Good Afternoon")
        print("Tell me how can I help you now?")
    else:
        speak("Hello,Good Evening")
        speak("Tell me how can I help you now?")
        print("Hello,Good Evening")
        print("Tell me how can I help you now?")

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = takeCommand().lower()
        if inp is None:
            continue
        if "quit" in inp or "good bye" in inp or "ok bye" in inp or "stop" in inp:
            speak('Good bye')
            print('Good bye')
            break
        else:
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                truncating='post', maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))
                    speak( np.random.choice(i['responses']))

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)