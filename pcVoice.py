Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@nivid26 
karan1199
/
Voice-controlled-PC-assistant
Public
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Voice-controlled-PC-assistant/Voice_PC.py /
@karan1199
karan1199 Add files via upload
Latest commit 967a7d5 on Sep 30, 2020
 History
 1 contributor
302 lines (223 sloc)  7.09 KB
   
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os.path
import os
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import time
import pyautogui
import webbrowser as wb
import datetime
import wikipedia
import keyboard
import sys
import subprocess


# In[2]:


NOTE = ["make a note", "write this down", "remember this", "type this"]
WEB = ["search","google"]
MAP=["open google map","open map","map","maps"]
EXIT = ["shutdown","goodbye","shut down","good bye"]
REMINDER = ["remind"]
WAKE="charlie"
recog = ""
start_stop = 0
google_URL="https://www.google.com/search?q="
youtube_URL = "http://www.youtube.com/results?search_query="
YOUTUBE =["youtube","play video"]
pyautogui.FAILSAFE =False
set_time=datetime.datetime.now()
NAME = "karan"


# In[3]:


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.say(text,rate-30)
    engine.runAndWait()


# In[4]:


def getaudio():
    global recog
    recog=""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
   
    try:
        recog = r.recognize_google(audio,language="en-IN")
        print("You said: " + recog)
        return recog.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return 0
    except sr.RequestError as e:
        print("Could not request; {0}".format(e)) 
        return 0
    
    
    


# In[5]:


def wakeaudio():
    global recog
    recog=""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
   
    try:
        recog = r.recognize_google(audio,language="en-IN")
        print("You said: " + recog)
    except Exception as e:
        print("Could not understand audio")
    return recog.lower()


# In[6]:


def web():
    speak("what do you want to search for")
    text=getaudio()
    if text !=0:
        wb.open(google_URL+text)
        speak("this is your result")
    else:
        speak("sorry,I coundn't understand please try again")
        web()
        
    
    
    


# In[7]:


def note():
    speak("What would you like me to write down? ")
    write_down = getaudio()
    if write_down != 0:
        date = datetime.date.today()
        file_name = str(date) + "-note.txt"
        with open(file_name, "a") as f:
            f.write(write_down+"\n")
            f.close()
        subprocess.Popen(["notepad.exe", file_name])
        speak("I've made a note of that.")
    else:
        speak("sorry,I coundn't understand please try again")


# In[8]:


def maps():
    speak("what do you want to search for")
    text=getaudio()
    if "between" in text:
        to=text.find("and")-1 
        froms=text.find("between") +8
        url=("https://www.google.com/maps/dir/"+text[froms:to]+"/"+text[to+5:])
        print(url)
        wb.open(url)
    elif "navigate" in text:
        text_new=text.split()
        text_temp=' '.join(text_new[2:])
        print(text_temp)
        wb.open("https://www.google.com/maps/dir/Current+Location/" + text_temp)
    else:
        speak("sorry try again")
        
        


# In[9]:


def wiki():
    speak("say the key word for information")
    text=getaudio()
    if text !=0:
        print(text)
        try:
            speak(wikipedia.summary(text,sentences=2))
        except DisambiguationError:
            speak("Sorry I dont know that")
    else:
        speak("sorry,I coundn't understand do you want to search again?")
        text=getaudio()

        if "yes" in text:
            wiki()        


# In[10]:


def youtube():
    
    speak("what video you want to search for?")
    text=getaudio()
    if text != 0:
        wb.open_new(youtube_URL+text)
        speak("this is your result and if you want to close it just say close youtube")
        pyautogui.click(450,580)
        while True:
            text = getaudio()
            if text!= 0:
                if "volume" in text:
                    if "up" in text:
                        pyautogui.press('up')
                    if "down" in text:
                        pyautogui.press('down')
                if "full screen" in text:
                    pyautogui.press('f')
                if "video speed" in text:
                    if "increase" in text:
                        pyautogui.hotkey('shift', '>')
                    if "decrease" in text:
                        pyautogui.hotkey('shift', '<')
                if "search" in text:
                    text_new = text.lstrip("search")
                    pyautogui.press('/')
                    for i in range(18):
                        pyautogui.press('backspace')
                    pyautogui.write(text_new)
                    pyautogui.press('enter')
                    time.sleep(4)
                    pyautogui.click(450,580)
                if "close youtube"  in text:
                    speak("closing youtube")
                    pyautogui.hotkey('ctrl', 'w')
                    break
    else:
        speak("sorry try again")
    


# In[11]:


def run():
    global start_stop
    global status 
    global remind
    global set_time
    while True:
        if start_stop==1:
            text = wakeaudio()
            if text.count(WAKE) > 0:
                print("Yes " + NAME)
                speak("Yes" + NAME)
                
                text = getaudio()
                if text!= 0:
                    for phrase in NOTE:
                        if phrase in text:
                            note()
                    for phrase in MAP:
                        if phrase in text:
                            maps()
                            text=""
                    for phrase in YOUTUBE:
                        if phrase in text:
                            youtube()
                    if "wikipedia" in text:
                        wiki()
                    for phrase in WEB:
                        if phrase in text:
                            web()
                    if "my computer" in text:
                        pyautogui.hotkey('win', 'e')
                        speak("okay")
                    if "desktop" in text:
                        pyautogui.hotkey('win', 'd')
                        speak("okay")
                    for phrase in EXIT:
                        if phrase in text:
                            start_stop=0
                            speak("bye for now")
                            
            
        else:
            while True:
                if keyboard.is_pressed('s'):
                        print("I am listening .. ")
                        speak("I am listening .. ")
                        start_stop=1
                        break


# In[ ]:


NAME_temp =pyautogui.prompt(text='Enter your name :', title='Voice controlled assistant' , default='Karan')
WAKE_temp =pyautogui.prompt(text='Enter bot name :', title='Voice controlled assistant' , default='Charlie')
if type(NAME_temp) is str and NAME_temp != "":
    NAME=NAME_temp.lower()
    
if type(WAKE_temp) is str and WAKE_temp != "":
    WAKE=WAKE_temp.lower()
    
     
print(WAKE)
print(NAME)   

while True:
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)


# In[ ]:





# In[ ]:



© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete
