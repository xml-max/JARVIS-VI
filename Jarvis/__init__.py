import speech_recognition as sr
import whisper
import datetime
import pyttsx3
import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Jarvis')))
from Jarvis.features import date_time
from Jarvis.features import launch_app
from Jarvis.features import website_open
from Jarvis.features import weather
from Jarvis.features import wikipedia
from Jarvis.features import news
from Jarvis.features import send_email
from Jarvis.features import google_search
from Jarvis.features import google_calendar
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc
from Jarvis.features import Game
from Jarvis.features import Server
from Jarvis.features import client
from Jarvis.features import AI_connector as ai
from Jarvis.features import phone_input
from TTS.api import TTS as CoquiTTS
from pydub import AudioSegment
from flask import request, jsonify  # <-- Needed for listen()
import tempfile                     # <-- Needed for listen()
import soundfile as sf              # <-- Needed for tts()
import sounddevice as sd            # <-- Needed for tts()
import Jarvis
import threading
import pvporcupine
import pyaudio
import struct
import queue
import threading
import sounddevice as sd
import numpy as np
import whisper
import re

WAKE_WORDS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

class JarvisAssistant:
    def listen_from_mic_whisper(self, model_size="base", active_mode_duration=10):
        """
        Blocking call: starts an offline Whisper-based listener, waits until
        wake-word + phrase are detected, then returns the recognized text.
        This function will block until speech is returned.
        """
        import queue
        import sounddevice as sd
        import numpy as np
        import whisper
        import time
        import threading
        import torch
        from rapidfuzz import fuzz

        class OfflineWhisperWakeWord:
            def __init__(self, model_path="base", wake_word="jarvis", active_mode_duration=10):
                self.model = whisper.load_model(model_path)
                self.wake_word = wake_word.lower()
                self.active_mode_duration = active_mode_duration
                self.audio_queue = queue.Queue()
                self.result_queue = queue.Queue()
                self.listening = True
                self.active = False
                self.last_active_time = 0
                self._stream = None

            def audio_callback(self, indata, frames, time_info, status):
                if status:
                    print("Audio error:", status)
                # copy to avoid referencing the same buffer
                self.audio_queue.put(indata.copy())

            def transcribe_chunk(self, audio_np):
                audio_np = whisper.pad_or_trim(audio_np.flatten())
                # send mel to device to avoid device mismatch
                mel = whisper.log_mel_spectrogram(audio_np).to(self.model.device)
                # transcribe (fp16 only if CUDA available)
                result = self.model.transcribe(audio_np, fp16=torch.cuda.is_available())
                return result["text"].lower().strip()

            def listen_loop(self):
                try:
                    with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=16000):
                        buffer = []
                        while self.listening:
                            try:
                                data = self.audio_queue.get()
                            except Exception:
                                continue
                            buffer.extend(data.flatten())

                            # process every ~2.5-3 seconds worth of audio
                            if len(buffer) >= 16000 * 3:
                                audio_chunk = np.array(buffer, dtype=np.float32)
                                buffer.clear()

                                try:
                                    text = self.transcribe_chunk(audio_chunk)
                                except Exception as e:
                                    print("[Transcription error]:", e)
                                    continue

                                if not text:
                                    continue

                                print("[Heard]:", text)

                                # If we are already in active mode, push recognized text
                                if self.active:
                                    # Put final text into result queue and continue active timer
                                    self.result_queue.put(text)
                                    self.last_active_time = time.time()
                                else:
                                    # Fuzzy check for wake word
                                    if fuzz.partial_ratio(self.wake_word, text) > 78:
                                        print("[Wake Word Detected] Entering active mode.")
                                        self.active = True
                                        self.last_active_time = time.time()
                                        # Put the phrase that contained the wake word
                                        self.result_queue.put(text)

                                # exit active mode after timeout
                                if self.active and (time.time() - self.last_active_time) > self.active_mode_duration:
                                    print("[System] Returning to passive mode.")
                                    self.active = False
                except Exception as e:
                    print("[InputStream error]:", e)
                    # Make sure listener stops on fatal stream error
                    self.listening = False

            def start(self):
                t = threading.Thread(target=self.listen_loop, daemon=True)
                t.start()

            def stop(self):
                # signal loop to stop
                self.listening = False

            def get_text(self, block=True, timeout=None):
                try:
                    if block:
                        return self.result_queue.get(timeout=timeout)  # blocks until something available
                    else:
                        return self.result_queue.get_nowait()
                except queue.Empty:
                    return None

        # --- run listener and block until a result is available ---
        listener = OfflineWhisperWakeWord(model_path=model_size, wake_word="jarvis", active_mode_duration=active_mode_duration)
        listener.start()

        try:
            # Block until a recognized phrase is put into the result_queue.
            # This will wait indefinitely until something is detected.
            recognized = listener.get_text(block=True, timeout=None)
            # After returning recognized text, stop the listener thread cleanly
            listener.stop()
            # small grace sleep to allow InputStream to close
            time.sleep(0.1)
            if recognized:
                # return the full recognized phrase (caller can post-process)
                return recognized
            else:
                return ""
        except KeyboardInterrupt:
            listener.stop()
            return ""
        except Exception as e:
            listener.stop()
            print("[listen_from_mic_whisper error]:", e)
            return ""

    def __init__(self):
        pass
    def phone(self):
        try:
            input = phone_input.start()  # Assuming phone_input.start() returns some input
        except Exception as e:
            print(e)
            input = None  # Handle the exception and decide what to return
        return input
    
    def ai_input(self, prompt, protocol_response="",bol=True):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')  # Fetch current time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fetch current date
        user_input = f"[prompt: \"{prompt}\", Time: \"{current_time}\", Date: \"{current_date}\", Protocol response: \"{protocol_response}\", Internet connection: \"{bol}\"]"
        
        try:
            ai_result,rawres = ai.chat(user_input)
            # If ai.chat returns a tuple, unpack it
            if isinstance(ai_result, tuple):
                ai_result = ai_result[0]
            response_text = ai_result.get('response_text', '')
            innerthought = ai_result.get('innerthought', '')
            protocol = ai_result.get('protocol', '')

            # Check for missing fields and handle errors
            if not response_text:
                response_text = "No response text available."
            if not innerthought:
                innerthought = "No inner thoughts available."
            if not protocol:
                protocol = "none"
            
            response = {
                'response_text': response_text,
                'innerthought': innerthought,
                'protocol': protocol
            }
            print(f"INIT: {response}")
            print()
            # Return all response details
            return response,rawres
        except Exception as e:
            # Handle any unexpected errors during AI communication
            response_text = "Sorry, something went wrong during processing."
            innerthought = f"Error: {str(e)}"
            protocol = "error"
            return {
                'response_text': response_text,
                'innerthought': innerthought,
                'protocol': protocol
            }


    def recognize_audio(self, file_path, model_size="base"):
        """
        Transcribe audio using Whisper.

        Args:
            file_path (str): Path to the audio file.
            model_size (str): Whisper model size - base, small, medium, large.

        Returns:
            str: Transcribed text or error message.
        """
        try:
            # Load the Whisper model (can be "base", "small", "medium", "large")
            model = whisper.load_model(model_size)
            # Transcribe the audio file
            result = model.transcribe(file_path)
            # Return the recognized text
            return result["text"]
        except Exception as e:
            # Return error message as string
            return f"Error during transcription: {e}"

    def mic_pc(self):
        """
        Fetch input from mic
        return: user's voice input as text if recognized, or "  " if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.adjust_for_ambient_noise(source, duration=1)  # Improve recognition in noisy environments
                r.energy_threshold = 400  # Lower threshold for more sensitivity
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            try:
                print("Recognizing...")
                command = r.recognize_google(audio, language='en-us').lower()
            except Exception as e:
                print('Recognition failed:', e)
                command = ""
            return command
        except Exception as e:
            print("Microphone/system error:", e)
            return False
        
    def tts(self, text):
        """
        Convert any text to speech
        :param text: text(String)
        :return: True/False (Play sound if True otherwise write exception to log and return  False)
        """
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()

        #print("TTS: ", text)

    def tell_me_date(self):

        return date_time.date()

    def tell_time(self):

        return date_time.time()

    def launch_any_app(self, path_of_app):
        """
        Launch any windows application 
        :param path_of_app: path of exe 
        :return: True is success and open the application, False if fail
        """
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)


    def weather(self, city):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 character from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    def news(self):
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        return news.get_google_news()
    
    def send_mail(self, sender_email, sender_password, receiver_email, msg):

        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)
        return 
        
        if date:
            return google_calendar.get_events(date, service)
        '''else:
            pass'''
    
    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)
    
    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country

    def game(self):
        Game.gem()
        
    def py_ssh_cli(self, command):
        client.execute_remote_command(host, port, command)
        
    def py_ssh_serv(host, port):
        Server.start_server(host, port)
        
obj = JarvisAssistant
