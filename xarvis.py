import os
import time

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr


VOLUME = 1
BEEP_DURATION = 0.4

def copy_to_clipboard(str, p=True, c=True):
    from subprocess import Popen, PIPE

    if p:
        p = Popen(['xsel', '-pi'], stdin=PIPE)
        p.communicate(input=str)
    if c:
        p = Popen(['xsel', '-bi'], stdin=PIPE)
        p.communicate(input=str)

def paste_to_active_screen(str):
	time.sleep(5)
	os.popen('xsel', 'wb').write(str)

def beep(vol=VOLUME, duration=BEEP_DURATION):
	command = "play -n synth {} sine 800 vol {}".format(duration, vol) 
	os.system(command)

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recognized = recognizer.recognize_google(audio)
        if recognized:
        	print("Clipped",recognized)	
        	copy_to_clipboard(recognized)
        	beep()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time
for _ in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
stop_listening() # calling this function requests that the background listener stop listening
while True: time.sleep(0.1)

