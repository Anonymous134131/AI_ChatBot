import speech_recognition as s
import pyttsx3 
import datetime
import time
import webbrowser
import requests
import json
import requests


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

        elif 'time' in statement:
            currentTime=datetime.datetime.now()
            ttime = currentTime.strftime("%c")
            print(f"The time is: {ttime}\n")
            speak(f"the time is {ttime}")

        elif 'search'  in statement:
            url = 'https://www.google.com/search?q='
            statement = statement.replace("search", "")
            webbrowser.open_new(url + statement)
            time.sleep(5)

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am a Simple ChatBot. I am programmed to do small tasks')

        elif "who made you" in statement or "who created you" in statement:
            speak(f"I was built by Ria, Dhruv and Alish")
            print(f"I was built by Ria, Dhruv and Alish")


        
        elif "weather" in statement or "forecast" in statement or "temperature" in statement:
            APIkey="88ee30e21293490d319a4a25ec3672fa"
            url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the name of the city")
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

        
        

