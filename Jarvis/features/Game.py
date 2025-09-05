import pyttsx3
import time
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def tts(text):
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 175)
def speak(text):
    tts(text)
def gem():
    p = print
    dict_app = {'Rock','Paper','Scissors'}
    dict_app_list = list(dict_app)
    sft=random.choice(dict_app_list)

    p("##########################################################################")
    p("Welcome to Rock paper scissors game")
    p("##########################################################################")

    speak("Welcome to Rock paper scissors game")
    p("1 rock \n2 paper\n3 scissors")
    speak("choose one please")

    int(usr=input("Choose one please: "))
    p("Rock")
    speak("Rock")
    p("Paper")
    speak("Paper")
    p("Sicssors")
    speak("Sicssors")
    p("Shoot")
    speak("Shoot")
    p(f"I choose "+sft)
    if usr == 1 and sft == "Rock":
        p("Tie")
        speak("Tie")
        speak("goodbye")
    elif usr == 2 and sft == "Paper":
        p("Tie")
        speak("tie")
        speak("goodbye")
    elif usr == 3 and sft == "Scissors":
        p("Tie")
        speak("TIE")
        speak("goodbye")
    elif usr == 1 and sft == "Scissors" or usr == 2 and sft == "Rock" or usr == 3 and sft == "Paper":
        p("You Win")
        speak("Okay,you win")
        speak("goodbye")
    elif usr == 1 and sft == "Paper" or usr == 2 and sft == "Scissors" or usr == 3 and sft == "Rock":
        p("I Won")
        speak("I won")
        speak("goodbye")
