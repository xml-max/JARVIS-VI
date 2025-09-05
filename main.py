print("Initializing User Interface please wait")
import logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
import sys
import traceback

def log_uncaught_exceptions(exctype, value, tb):
    with open("fatal.log", "a") as f:
        traceback.print_exception(exctype, value, tb, file=f)
    print("🔥 A fatal exception occurred. Check fatal.log for details.")

sys.excepthook = log_uncaught_exceptions

#+==============================================Imports=================================================+
from Jarvis import JarvisAssistant
import os
import sys
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import pdb
import threading
try:
    import pywhatkit
except Exception as e:
    pass
import wolframalpha
from PIL import Image
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config
from Jarvis import __init__
from Jarvis.features import Server
import subprocess
import sqlite3
# import ch
import socket
import guiold as gui
from queue import Empty
from queue_shared import voice_command_queue, response_queue
from queue import Queue
import threading
import sounddevice as sd
import soundfile as sf
from TTS.api import TTS as CoquiTTS

__all__ = ["voice_command_queue", "response_queue"]

#+==============================================Imports=================================================+

#+==============================================Authentication=Process==============================================+

# from fingerprint import auth

# authentication = auth()
# if authentication:
#     JarvisAssistant.tts(self='',text="Access Authorized")
# else:
#     sys.exit('Access Unauthorized')

#+==================================================================================================================+

def init_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    return server_socket

obj = JarvisAssistant()
# ================================ MEMORY ==========================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'abdelrahmanhatem338@gmail.com',
    'baba' : 'drhatemdentnote9@gmail.com'
}
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
Time = ["what time is it","tell me the time","what is the time","what is the date", "what is today's date","what is today date","tell me the date", "the date", "weather", "tell me about", "where is", "take screenshot", "show screenshot"]
# =======================================================================================================================================================
 #this was for testing
# usr_choice=ch.get_user_input()

# print(usr_choice)
# def mic_input(usr_choice):
#     if usr_choice == 1:
#         inputis = obj.phone()  # Assuming obj.phone() returns some input
#         #print('111')
#     elif usr_choice == 0:
#         inputis = obj.mic_pc()
#         #print('0000')
#     elif usr_choice == 2:
#         inputis = input("Type what you want: ")
#     elif usr_choice == "EXIT":
#         inputis = None
#         print("Exiting...")
#         sys.exit()
#     else:
#         inputis = None  # Adjust this based on what should happen when usr_choice is neither 0 nor 1
#     return inputis

#while True:
    #print(obj.ai_input(mic_input(ch.get_user_input())))

def internet():
    try:
        import pywhatkit
        bol=True
    except:
        bol= False
    return bol


# === TTS QUEUE AND WORKER ===
try:
    if config.TTS_ENGINE.lower() == "offsline" or config.TTS_ENGINE.lower() == "coqui":
        coqui_tts_model = CoquiTTS("tts_models/multilingual/multi-dataset/xtts_v2")
        TTS = "OFFLINE"
except Exception as e:
    print(f"Failed to load Coqui TTS model: {e}")

def speak(text):
    if config.TTS_ENGINE.lower() == "offline" or config.TTS_ENGINE.lower() == "coqui":
        print(f"[TTS] Speaking: {text}")
        coqui_tts_model.tts_to_file(
            text=text,
            speaker_wav=r"C:\Users\Abdelrahman_Hatem\Desktop\Python Projects\JARVIS-mk.1\JARVIS-master\jarvis_sample.wav",
            language="en",
            file_path="output.wav"
        )
        data, fs = sf.read("output.wav")
        sd.play(data, fs)
        sd.wait()

    else:
        obj.tts(text)

speak("Initializing Jarvis, please wait...")

def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None
    
def startup():
    import os
    os.system("cls")
    # speak("Initializing Jarvis")
    from Jarvis import __init__
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    bol=internet()
    if bol == True:
        """speak("pinging google.com")
        import os
        hostname = "google.com" 
        response = os.system("ping -c 1 " + hostname)
        os.system("cls")"""
        speak("connected to the internet")
    else:
        speak("There is no Internet connection, proceeding with the local connections")
    speak("connecting to the database")
    conn = sqlite3.connect("lessons.db")
    cursor = conn.cursor()
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("systems are now fully operational")
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    if hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    c_time = c_time.split(':')
    ctime = f"{c_time[0]} hours {c_time[1]} minutes and {c_time[2]} seconds"
    
    speak(f"Currently it is {ctime}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
    



def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    if hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")
# if __name__ == "__main__":

class MainThread(QThread):
    def __init__(self, bridge=None):
        super().__init__()
        self._running = True
        self.bridge = bridge

    def log(self, msg):
        print(msg)
        if self.bridge:
            self.bridge.log_to_ui(msg)

    def run(self):
        self._running = True
        try:
            startup()
            self.log("🔥 MainThread started")
            self.TaskExecution()
        except Exception as e:
            print("🚨 Exception in run():", e)
            import traceback
            traceback.print_exc()


    def stop(self):
        self._running = False
        self.wait()

    def TaskExecution(self):
        print ("Starting Jarvis Assistant")
        # startup()
        print("")
        while self._running:
            try:
                mic = obj.listen_from_mic_whisper() if config.SR_ENGINE.lower() == "whisper" else obj.mic_pc()  # Wait up to 1 sec
            except Empty:
                continue  
            if not mic:
                continue  # Skip if blank or silence

            self.log(f"🗣️ User said: {mic}")
            #print(f"User said: {mic}")

            print("")
            try:
                timee = datetime.datetime.now().strftime('%H:%M:%S')
                timee = str(timee)
                bol = internet()
                ai_response = obj.ai_input(mic, ' ', bol)
                def ai_parser(ai_response):
                    if isinstance(ai_response, tuple) and len(ai_response) == 2:
                        ai_response, rawres = ai_response
                    else:
                        rawres = None
                    response_text = ai_response.get('response_text', rawres) if isinstance(ai_response, dict) else str(ai_response)
                    innerthought = ai_response.get('innerthought', 'No inner thoughts available.') if isinstance(ai_response, dict) else ''
                    protocol = ai_response.get('protocol', 'none') if isinstance(ai_response, dict) else 'none'
                    return response_text, innerthought, protocol
                response_text, innerthought, protocol = ai_parser(ai_response)
                print(f"Response Text: {response_text}")
                print(f"Inner Thought: {innerthought}")
                print(f"Protocol: {protocol}")

                commandai = protocol.lower()
                response = response_text
                speak(response)
            except Exception as e:
                import traceback
                commandai = "This is Exception handler, Please start AI server. just use cmd and type ollama serve or navigate to the website for more info"
                print(f"use ollama serve in the cmd: error code: {e}")
                traceback.print_exc()
                print(e)
                continue  # Ensure the loop continues even after an exception

            if True:
                command = commandai.lower()
                if command in GREETINGS:
                    speak(random.choice(GREETINGS_RES))
                if "start ssh server" in command:
                    speak("starting ssh server sir")
                    Server.start_server(host="192.168.1.45", port=12345)
                if "shutdown remote server" in command:
                    obj.py_ssh_cli(command="shutdown /s")
                if "reboot the remote server" in command:
                    obj.py_ssh_cli(command="shutdown /r")
                if "list directory files" in command:
                    obj.py_ssh_cli(command="ls -al")
                # Replace re.search('open', command) with a simple substring check
                if "open" in command:
                    domain = command.split(' ')[-1]
                    open_result = obj.website_opener(domain)
                    speak(f'Alright sir !! Opening {domain}')
                    print(open_result)
                if "reboot" in command:
                    os.system("shutdown /r /t 3")
                if "hibernate" in command:
                    os.system("shutdown /h /t 3")
                if "lock" in command:
                    os.system("shutdown /l")
                if "emergency shutdown" in command:
                    os.system("shutdown /p")

                if "what can you do" in command:
                    speak("i can help you with your daily tasks like reading your schedule and helping you with your homework")
                    speak("i can also help you with some calculations ")
                    speak("i can help you with many other things i,ll mention it later")
                    speak("i'll be here 24hour a day,7days a week")

                if "buzzing" in command or "news" in command or "headlines" in command:
                    print("[DEBUG] News protocol is Fetching ")
                    news_res = obj.news()
                    print("[DEBUG] News protocol is being executed")
                    print()
                    speak('Source: Google News')
                    speak('Todays Headlines are being summarized')
                    # First AI call: get protocol response
                    resp, raw = obj.ai_input(
                        prompt='',
                        protocol_response=f"This is the fetched raw news that i want you to summarize and give me your opinion {news_res}."
                    )
                    print("[DEBUG] Full AI response object:", resp)
                    print("[DEBUG] Raw AI response:", raw)
                    response_text, innerthought, protocol = ai_parser(resp)
                    print(f"[DEBUG] Protocol after first AI call: {protocol}")
                    # If protocol is still 'news', do a second AI call with the news as protocol_response
                    if protocol == "news":
                        print("[DEBUG] Protocol is still 'news', sending protocol_response with news to AI again.")
                        resp2, raw2 = obj.ai_input(
                            prompt='STRICT TO YOUR RESPONSE FORMAT',
                            protocol_response=news_res
                        )
                        print("[DEBUG] Second AI response object:", resp2)
                        print("[DEBUG] Second Raw AI response:", raw2)
                        response_text, innerthought, protocol = ai_parser(resp2)
                        if protocol == "error":
                            import re, json
                            print("[DEBUG] AI returned protocol 'error', attempting to extract JSON from raw response:")
                            print(raw2)
                            match = re.search(r"\{[\s\S]*\}", raw2)
                            if match:
                                try:
                                    json_block = match.group(0)
                                    parsed = json.loads(json_block)
                                    articles = parsed.get("articles", [])
                                    if articles:
                                        summary = []
                                        for art in articles:
                                            title = art.get("title", "")
                                            desc = art.get("description", "")
                                            url = art.get("url", "")
                                            summary.append(f"Title: {title}\nDescription: {desc}\nURL: {url}")
                                        summary_text = "\n\n".join(summary)
                                        print(summary_text)
                                        speak(summary_text)
                                    else:
                                        print(json_block)
                                        speak(json_block)
                                except Exception as e:
                                    print("[DEBUG] Failed to parse JSON from raw response:", e)
                                    print(raw2)
                                    speak(raw2)
                            else:
                                print(raw2)
                                speak(raw2)
                        else:
                            print(response_text)
                            speak(response_text)
                    else:
                        if protocol == "error":
                            import re, json
                            print("[DEBUG] AI returned protocol 'error', attempting to extract JSON from raw response:")
                            print(raw)
                            match = re.search(r"\{[\s\S]*\}", raw)
                            if match:
                                try:
                                    json_block = match.group(0)
                                    parsed = json.loads(json_block)
                                    articles = parsed.get("articles", [])
                                    if articles:
                                        summary = []
                                        for art in articles:
                                            title = art.get("title", "")
                                            desc = art.get("description", "")
                                            url = art.get("url", "")
                                            summary.append(f"Title: {title}\nDescription: {desc}\nURL: {url}")
                                        summary_text = "\n\n".join(summary)
                                        print(summary_text)
                                        speak(summary_text)
                                    else:
                                        print(json_block)
                                        speak(json_block)
                                except Exception as e:
                                    print("[DEBUG] Failed to parse JSON from raw response:", e)
                                    print(raw)
                                    speak(raw)
                            else:
                                print(raw)
                                speak(raw)
                        else:
                            print(response_text)
                            speak(response_text)
                    
                    speak('These were the top headlines, Have a nice day Sir!!..')
                    #speak("this feature is coming soon")

                if 'search google for' in command:
                    obj.search_anything_google(command)
                if 'tell me the day' in command:
                    now = datetime.datetime.now()
                    print(now.strftime("%A"))
                    speak ("it's " + now.strftime("%A"))
                if 'introduce yourself' in command :
                    speak("let me introduce myself, i,m jarvis, your virtual artifitial intelegence, and i'm here to assist you with veroity of tasks as best as i can, 24 hours a day,7 days a week, system is now fully operational")
                if "play music" in command or "hit some music" in command:
                    music_dir = "F://Songs//Imagine_Dragons"
                    songs = os.listdir(music_dir)
                    for song in songs:
                        os.startfile(os.path.join(music_dir, song))

                if 'youtube' in command:
                    video = command.split(' ')[1]
                    speak(f"Okay sir, playing {video} on youtube")
                    pywhatkit.playonyt(video)

                if "email" in command or "send email" in command:
                    sender_email = config.email
                    sender_password = config.email_password

                    try:
                        speak("Whom do you want to email sir ?")
                        recipient = obj.mic_input()
                        receiver_email = EMAIL_DIC.get(recipient)
                        if receiver_email:

                            speak("What is the subject sir ?")
                            subject = obj.mic_input()
                            speak("What should I say?")
                            message = obj.mic_input()
                            msg = 'Subject: {}\n\n{}'.format(subject, message)
                            obj.send_mail(sender_email, sender_password,
                                          receiver_email, msg)
                            speak("Email has been successfully sent")
                            time.sleep(2)

                        else:
                            speak(
                                "I coudn't find the requested person's email in my database. Please try again with a different name")

                    except:
                        speak("Sorry sir. Couldn't send your mail. Please try again")

                if "calculate" in command:
                    question = command
                    answer = computational_intelligence(question)
                    speak(answer)
                if "can we play a game " in command or "play game" in command:
                    speak("starting a game, please navigate to debug console")
                    obj.game()
                    os.system("cls")

                    
                    cmd = command
                    if "start simulation" in cmd:
                        speak("starting simulation")
                        simmode = 1
                        return simmode
                    
                    if "end simulation" in cmd or "stop simulation" in cmd:
                        speak("stopping simulation")
                        simmode = 0
                        return simmode

                    if "activate game defencemode" in command or "activate game defence mode" in command:
                        speak("activating game defence mode")
                        speak("activating drones")
                        speak("drones are online")
                        speak("defending the base from unathorised persons")
                            
                    if "activate attack mode" in command or "activate attackmode" in command:
                        speak("activating game defence mode")
                        speak("activating drones")
                        speak("drones are online")
                        speak("attacking the targets sir")
                if "what is" in command or "who is" in command:
                    question = command
                    answer = computational_intelligence(question)
                    speak(answer)

                if "what do i have" in command or "do i have plans" in command or "am i busy" in command:
                    now = datetime.datetime.now()
                    day = now.strftime("%A")
                    if day == "Friday":
                        speak("you are free sir")
                    if "Saturday" in day or "Tuesday" in day:
                        speak("You have the Math lesson at 7pm")
                        
                    if "Sunday" in day or "Wednesday" in day:
                        speak("you have Arabic lesson at 7pm")
                        
                    if "Monday" in day or "Thursday" in day:
                        speak("you have an english lesson at 11.30am")
                        speak("you have social studies at 6:50pm")
                        speak("you have science at 8pm ")

                if "make a note" in command or "write this down" in command or "remember this" in command:
                    speak("What would you like me to write down?")
                    note_text = obj.mic_input()
                    obj.take_note(note_text)
                    speak("I've made a note of that")

                if "close the note" in command or "close notepad" in command:
                    speak("Okay sir, closing notepad")
                    os.system("taskkill /f /im notepad++.exe")
                    
                if "joke" in command:
                    joke = pyjokes.get_joke()
                    print(joke)
                    speak(joke)

                if "system_stats" in command:
                    sys_info = obj.system_info()
                    #print(sys_info)
                    ai_result = obj.ai_input(
                        prompt='',
                        protocol_response=f"[PROTOCOL EXECUTER] this is the system stats: {sys_info} make some recommendations and decide whether it needs anything to be done do it"
                    )
                    # ai_input returns (dict, rawres), so unpack it first
                    if isinstance(ai_result, tuple):
                        ai_result, _ = ai_result
                    response = ai_result.get('response_text', '')
                    inner = ai_result.get('innerthought', '')
                    protocol = ai_result.get('protocol', '')
                    print(f"AI Response: {response!r}")  # Use repr to show even empty/whitespace
                    print(f"AI Innerthought: {inner!r}")
                    print(f"AI Protocol: {protocol!r}")
                    speak(response)
                    
                if "shutdown" in command or "shut down" in command:
                    os.system("shutdown /s /t 3")
                if "database" in command:
                    now = datetime.datetime.now()
                    day = now.strftime("%A")
                    if "Saturday" in day or "Tuesday" in day:
                        idn = str(1)
                        
                    if "Sunday" in day or "Wednesday" in day:
                        idn = str(2)
                        
                    if "Monday" in day or "Thursday" in day:
                        idn = str(3)
                    conn = sqlite3.connect("lessons.db")
                    cursor = conn.cursor()
                    cursor.execute("select * from lessons where id="+idn)
                    result = cursor.fetchall()
                    results = str(result)
                    speak("according to the database you have" + results)
                    print("according to the database you have\n" + results)

                if "ip address" in command:
                    ip = requests.get('https://api.ipify.org').text
                    print(ip)
                    speak(f"Your ip address is {ip}")
                if "test" in command or "make sure every thing is working" in command :
                    speak("ok sir testing all system applications")
                    try:
                        obj.tts(text="test")
                        obj.tell_me_date()
                        obj.tell_time()
                        obj.website_opener(domain="youtube.com")
                        obj.weather(city="Tahta")
                        obj.tell_me(topic="J.A.R.V.I.S")
                        speak("skipping send email and other applications")
                        obj.system_info()
                        obj.location(location="tahta")
                        obj.my_location()
                    except Exception as e:
                        print(e)
                        speak("some exception occur")
                if "close the window" in command or "close window" in command:
                    speak("okay sir, closing the window")
                    pyautogui.keyDown("alt")
                    pyautogui.press("f4")
                    time.sleep(1)
                    pyautogui.keyUp("alt")
                if "switch the window" in command or "switch window" in command:
                    speak("Okay sir, Switching the window")
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")

                if "where i am" in command or "current location" in command or "where am i" in command:
                    try:
                        city, state, country = obj.my_location()
                        print(city, state, country)
                        speak(obj.ai_input(f"You are currently in {city} city which is in {state} state and country {country}"))
                    except Exception as e:
                        speak(
                            "Sorry sir, I coundn't fetch your current location. Please try again")

                
                if "hide all files" in command or "hide this folder" in command:
                    os.system("attrib +h /s /d")
                    speak("Sir, all the files in this folder are now hidden")

                if "visible" in command or "make files visible" in command:
                    os.system("attrib -h /s /d")
                    speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

                # if "calculate" in command or "what is" in command:
                #     query = command
                #     answer = computational_intelligence(query)
                #     speak(answer)

                

                if "exit" in command:
                    speak("Alright sir, shutting down systems. It was nice working with you")
                    speak("Stopping all systems applications")
                    speak("Stopping all drivers")
                    speak("Shutting down all the core processors")
                    speak("Disconnecting from the database")
                    speak("All drivers are down")
                    speak("All systems have been deactivated")
                    speak("Systems are now offline")
                    kill
                    sys.exit()
                else:
                    print("Normal Just procceed")
                    pass
            if command.lower() in Time:
                found = True
                if "date" in command:
                    current_date = obj.tell_me_date()
                    print(current_date)
                    speak(current_date)
                if "time" in command:
                    current_time = obj.tell_time()
                    print(current_time)
                    speak(f"Sir the time is {current_time}")
                if "weather" in command:
                    q = command.split(' ')[-1]
                    if "" in q or " " in q:
                        city, state, country = obj.my_location() 
                        weather_res = obj.weather(city=city)
                        print(weather_res)
                        speak(weather_res)
                    else:
                        city = command.split(' ')[-1]
                        weather_res = obj.weather(city=city)
                        print(weather_res)
                        speak(weather_res)
                # Also, for 'tell me about', replace re.search with substring check
                if "tell me about" in command:
                    topic = command.split(' ')[-1]
                    if topic:
                        ai_response = obj.ai_input(
                            f"explain this to me i got it from wikipedia {obj.tell_me(topic)}",
                            time=datetime.datetime.now().strftime("%H:%M:%S"),
                            date=datetime.datetime.now().strftime("%Y-%m-%d")
                        )
                        wiki_res = ai_response['response_text']
                        print(wiki_res)
                        speak(wiki_res)
                if "where is" in command:
                    place = command.split('where is ', 1)[1]
                    current_loc, target_loc, distance = obj.location(place)
                    city = target_loc.get('city', '')
                    state = target_loc.get('state', '')
                    country = target_loc.get('country', '')
                    time.sleep(1)
                    try:
                        if city:
                            res = f"{place} is in {state} state and country {country}. It is {distance} km away from your current location"
                            print(res)
                            speak(res)
                        else:
                            res = f"{state} is a state in {country}. It is {distance} km away from your current location"
                            print(res)
                            speak(res)
                    except:
                        res = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                        speak(res)
                if "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                    speak("By what name do you want to save the screenshot?")
                    name = voice_command_queue.get(timeout=1)
                    speak("Alright sir, taking the screenshot")
                    img = pyautogui.screenshot()
                    name = f"{name}.png"
                    img.save(name)
                    speak("The screenshot has been succesfully captured")
                if "show screenshot" in command:
                    try:
                        img = Image.open(name)
                        img.show(img)
                        speak("Here it is sir")
                        time.sleep(2)
                    except IOError:
                        speak("Sorry sir, I am unable to display the screenshot")
            else:
                pass

# Remove this line, as it is incorrect and causes the TypeError:
# threading.Thread(target=MainThread.run).start()

"""if __name__ == "__main__":
 
    threading.Thread(target=gui.run_ui,daemon=True).start()

    # Start Jarvis assistant
    main_thread = MainThread()
    main_thread.start()

    # Step 3: Start main logic thread
    main_thread.wait()
    """

    
startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
label_date = current_date.toString(Qt.ISODate)
self.ui.textBrowser.setText(label_date)
self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
