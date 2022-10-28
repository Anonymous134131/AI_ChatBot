import speech_recognition as s
import pyttsx3 
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha

texttospeech = pyttsx3.init('sapi5')
texttospeech.setProperty('voice', texttospeech.getProperty('voices')[0].id)

def speak(text):
    texttospeech.say(text)
    texttospeech.runAndWait()

def takeCommand():
    r=s.Recognizer()
    with s.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

if __name__=='__main__':

    while True:
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
        
        statement = takeCommand().lower()
        if statement is None:
            continue
        if "hello" in statement or "hey" in statement:
            speak("Hello")
            print("Hello")
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Good bye')
            print('Good bye')
            break
        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'ask' in statement:
            speak("I can answer omputational and geographical questions")
            question=takeCommand()
            appid = "2WGHR5-HHQ78XU44V"
            client = wolframalpha.Client("2WGHR5-HHQ78XU44V")
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        
        elif "log off" in statement or "signout" in statement:
            speak("Your PC will log off in 10 seconds, please close all you applications")
            subprocess.call(["shutdown", "/h"])

time.sleep(3)
