#!/usr/bin/python
import collections
import difflib
import logging
import os
import random
import time
import webbrowser

import pyttsx
import pyperclip
import duckduckgo
import speech_recognition as sr

import super_scrape

from capabilities import (
    copy_to_clipboard,
    paste_to_active_screen,
    browse)
from utils import beep, execute_command
from conf import settings



GOOGLE_SEARCH_URL = "https://www.google.com/search?q={}"
GOOGLE_INSITE_SEARCH = "https://www.google.com/#q=site:{}+{}&*"
YOUTUBE_URL = "http://www.youtube.com/results?q={}"
SOUNDCLOUD_URL = "https://soundcloud.com/search?q={}"

recognized_keywords = settings.keys()

# keeps prev value of the clipped items
clipboard = collections.deque(maxlen=4)

def process_recognized_string(r):
    # Do all the preprocessing
    r = r.lower()
    r = r.split(' ')

    start_word = r[0]
    rest_word = " ".join(r[1:])

    # Keyword matching
    if match_intent(start_word, "google", "search", "find"):
        url = GOOGLE_SEARCH_URL.format(rest_word)
        browse(url)

    elif match_intent(start_word, "hi", "hello", "good", "hey"):
        print("greeting")
        speak(greeting_message())

    elif match_intent(start_word, "youtube", "watch"):
        url = YOUTUBE_URL.format(rest_word)
        browse(url)

    elif match_intent(start_word, "error", "debug", "stack", "stackoverflow"):
        in_site_search("stackoverflow.com", clipboard[-2])

    elif match_intent(start_word, "execute", "run"):
        # run command
        pass

    elif match_intent(start_word, "tell", "talk", "talkback"):
        # get results from google and speak them
        if start_word=="tell" and r[1] =="me":
            instant_answer(" ".join(r[2:]))
        else:
            instant_answer(rest_word)

    elif match_intent(start_word, "sing", "listen"):
        url = SOUNDCLOUD_URL.format(rest_word)
        browse(url)

    elif match_intent("dirty"):
        # ghetto talk
        pass

    #this one is supercool
    elif start_word=="auto" and r[1] == "play" or start_word=="autoplay":
        print("inside")
        vid_description = rest_word
        if r[1] == "play":
            vid_description = " ".join(r[2:])
        url = super_scrape.youtube_first_search_result(vid_description)
        if url:
            browse(url)

    else:
        matches = difflib.get_close_matches(start_word, recognized_keywords)
        if matches:
            keyword = matches[0]
            print(keyword)
            setting = settings[keyword]
            val = setting["value"]
            setting_type = setting["type"]

            if setting_type == "os":
                execute_command(val)
            
            elif setting_type == "browser":
                browse(val)
            
            elif setting_type == "browser_parametric":
                browse(val.format(rest_word))
            
            elif setting_type == "python":
                if type(val) == dict:
                    setting["function"](**val)
                else:
                    setting["function"]()

            #TODO
            elif setting_type == "notify":
                if type(val) == dict:
                    setting["function"](**val)
                else:
                    setting["function"]()

def match_intent(s, *possibilities):
    if difflib.get_close_matches(s, possibilities):
        return True
    return False

def callback(recognizer, audio):
    try:
        recognized = recognizer.recognize_google(audio)
        if recognized:
            logging.info("clipped"+recognized+"\n")
            copy_to_clipboard(recognized)
            logging.info("copied text to clipboard.")
            beep()
            process_recognized_string(recognized)
        return recognized
    
    except sr.UnknownValueError:
        print("..")
    
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def copy_to_clipboard(text):
    current = pyperclip.paste()
    if (not clipboard) or (clipboard and clipboard[-1]!=current):
        clipboard.append(current)
    pyperclip.copy(text)
    clipboard.append(text)

def in_site_search(site, q):
    url = GOOGLE_INSITE_SEARCH.format(site,q)
    browse(url)

def speak(text):
    engine = pyttsx.init()
    if type(text) == list:
        for t in text:
            engine.say(t)
    else:
        engine.say(text)
    engine.runAndWait()

def instant_answer(question):
    r = duckduckgo.query(question)
    ans = r.abstract.text
    speak(ans)

def random_quote():
    quotes = []
    with open("quotes.txt", "r") as f:
        quotes = f.readlines()
    return random.choice(quotes)

def greeting_message():
    salutation = ["Hi", "Hello", "Hey", "Whats up", "Yo"]
    time_greet_begin = ["Good", "Wonderful", "Awesome"]
    time_greet = ""

    currentTime = int(time.strftime('%H:%M').split(':')[0])   
    if currentTime < 12 :
         time_greet = "morning"
    if currentTime > 12 :
         time_greet = "afternoon"
    if currentTime > 6 :
         time_greet = "evening"

    name = ["Satwik", "captain", "master", "dude", "brother"]
    quote = random_quote()

    start_text = random.choice([random.choice(salutation),
                               random.choice(time_greet_begin)+time_greet]) + random.choice(name)


    middle_text = "Here's a quote for you"
    
    end_text = quote

    return [start_text, middle_text, quote]





if __name__ == "__main__":
    logging.basicConfig(filename='output.log',level=logging.INFO)
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some other computation for 5 seconds, then stop listening and keep doing other computations
    for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
    #stop_listening()  # calling this function requests that the background listener stop listening
    while True: time.sleep(0.1)

