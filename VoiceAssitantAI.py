from queue import Empty
import speech_recognition as s
import pyttsx3 
import datetime

texttospeech = pyttsx3.init('sapi5')
texttospeech.setProperty('voice', texttospeech.getProperty('voices')[1].id)

def speak(text):
    texttospeech.say(text)
    texttospeech.runAndWait()

def takeCommand():
    recognizer= s.Recognizer()
    microphone = s.Microphone()
    while True:
        print("Listening...")
        audio= recognizer.listen(microphone)
        try:
            statement=recognizer.recognize_google(audio,language='en-in')
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