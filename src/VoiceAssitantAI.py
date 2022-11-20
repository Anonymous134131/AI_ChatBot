from queue import Empty
import re
from bs4 import BeautifulSoup
import speech_recognition as s
import pyttsx3 
import datetime
from queue import Empty
import urllib.request
import wikipedia
import webbrowser
import requests
import json
import os
import time
import subprocess
import wolframalpha
import numpy as np
import tflearn
import tensorflow as tf
import random
import nltk
from nltk.stem.lancaster import LancasterStemmer

from train_model import train_model

stemmer = LancasterStemmer()
texttospeech = pyttsx3.init('sapi5')

texttospeech.setProperty('voice', texttospeech.getProperty('voices')[0].id)

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
    r=s.Recognizer()
    with s.Microphone() as source:
        print(Fore.CYAN + "Listening..." + Style.RESET_ALL)
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
            print(statement)

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


model = train_model()
def clean_up_sentence(sentence):

    sentence_words = nltk.word_tokenize(sentence)

    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

    # return bag of words array
def bow(sentence, words, show_details=False):

    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


def classify(sentence):
    # generate probabilities from the model
    results = model.model.predict([bow(sentence, model.words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>model.ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((model.classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in data['intents']:
                if i['tag'] == results[0][0]:
                    return random.choice(i['responses'])

            results.pop(0)


def initialGreeting():
    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
    hour=datetime.datetime.now().hour
    if hour>0 and hour<12:
        print('Hello, Good Morning')
        print("Please tell me how can I help you?")
        speak("Hello, Good Morning,")
        speak("Please tell me how can I help you?")
    elif hour>=12 and hour<18:
        print("Hello,Good Afternoon")
        print("Please tell me how can I help you?")
        speak("Hello,Good Afternoon")
        speak("Please tell me how can I help you?")
    else:
        print("Hello,Good Evening")
        print("Please tell me how can I help you?")
        speak("Hello,Good Evening")
        speak("Please tell me how can I help you?")


if __name__=='__main__':
    initialGreeting()
      
    while True:
        # print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = takeCommand().lower()
        # print(inp)
        if inp is None:
            continue
        if "quit" in inp or "exit" in inp or "good bye" in inp or "ok bye" in inp or "stop" in inp: #Test this, there might be some error with the AI not exiting after exit [statment(s)/word(s)] have been spoken
            speak('Good bye')
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            print('Good bye')
            break

        elif 'time' in inp:
            currentTime=datetime.datetime.now()
            ttime = currentTime.strftime("%c")
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            print(f"The time is: {ttime}\n")
            speak(f"the time is {ttime}")

        elif 'search'  in inp:
            url = 'https://www.google.com/search?q='
            inp = inp.replace("search", "")
            speak("Opening Browser with your search")
            print("Opening Browser with your search")
            webbrowser.open_new(url + inp)

        elif 'wikipedia' in inp:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            speak('Please wait, searching wikipedia...')
            #inp = inp.replace("wikipedia", "")
            results = wikipedia.summary(inp.replace("wikipedia", ""), sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in inp:
            webbrowser.open_new_tab("https://www.youtube.com")
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            speak("Please wait, opening youtube")
            speak("youtube is now open")
            print("youtube is now open")
            time.sleep(5)
        
        elif 'play' in inp and 'on youtube' in inp:
            search_words = inp.replace("play",'')
            search_words = search_words.replace("on youtube", '')
            search_words.strip()
            words = search_words.split()
            search_link = "http://www.youtube.com/results?search_query=" + '+'.join(words)
            print(search_link)
            html = urllib.request.urlopen(search_link)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            if not video_ids:
                raise KeyError("No video found")
            link = "https://www.youtube.com/watch?v=" + video_ids[0]
            print(link)
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            speak("Please wait, searching video")
            speak("opening video")
            print("loading completed")
            webbrowser.open_new(link)
            
            time.sleep(5)

        elif 'open gmail' in inp:
            webbrowser.open_new_tab("gmail.com")
            speak("Please wait, opening google mail")
            speak("Google Mail now open")
            time.sleep(5)
            print("Goolge Mail (Gmail) is now open")
        elif 'computational and geographical questions' in inp or 'computational and geographical question' in inp or 'computational questions' in inp or 'computational questions' in inp or 'geographical question' in inp or 'geographical questions' in inp:
            speak("Please ask me your computational and geographical question")
            question=takeCommand()
            appid = "2WGHR5-HHQ78XU44V"
            res = wolframalpha.Client(appid).query(question)
            answer = next(res.results).text
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            print(answer)
            #If the question is out of computational and geographical scope code [currentlly this block of code is under development]
            #if answer == None: 
               #speak("Sorry information is not found")
                #print("Sorry, Iinformation is not found")
            #else:
            speak(answer)
        elif "log off" in inp or "signout" in inp:
            speak("Your PC will log off in 10 seconds, please close all you applications")
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            print("Your PC will log off in 10 seconds, please close all you applications")
            subprocess.call(["shutdown", "/h"])
        
        elif "weather" in inp or "forecast" in inp or "temperature" in inp:
            APIkey="88ee30e21293490d319a4a25ec3672fa"
            url="https://api.openweathermap.org/data/2.5/weather?"
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            speak("what is the name of the city")
            print("what is the name of the city")
            
            city=takeCommand()
            urlLink=url+"appid="+APIkey+"&q="+city
            answer = requests.get(urlLink)
            weatherToday=answer.json()
            if weatherToday["cod"]!="404":
                today=weatherToday["main"]
                weather = today["temp"]                
                value = weatherToday["weather"]
                weather_description = value[0]["description"]
                speak(f" Temperature in kelvin unit is " +
                      str(weather))
                print(f" Temperature in kelvin unit = " +
                      str(weather))
            else:
                speak(" City Not Found ")
        else:
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            # print(inp)
            results = [result[1] for result in classify(inp)]
            responseString = '' 
            for value in results:
                if value >= 0.8:
                    # print("Match found: ", float(value)*100 ,"%")
                    responseString= response(inp)
                    print(responseString)
                    speak(responseString)
                    break 
        
            # print("Possible Match percent: ", float(value)*100 ,"%")
            if not responseString and inp is not None:
                print("Sorry I did not find any information regarding this in our database! Do you want to search on internet")
                speak("Sorry I did not find any information regarding this in our database! Do you want to search on internet")
                confirmation_command = takeCommand().lower()
                if "yes" in confirmation_command or "ya" in confirmation_command or "yeah" in confirmation_command or "yup" in confirmation_command:
                    inp.replace("what is",'')
                    results = wikipedia.summary(inp, sentences=5)
                    print("This is what I found on Internet: ")
                    speak("This is what I found on Internet")
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                else:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
                    print("Okay")
                    speak("Okay")
    
            print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,end="")
            speak("Is there anything else I could do for you?")
            print("Is there anything else I could do for you?")
            
       
    
print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)