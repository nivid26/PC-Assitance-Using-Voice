import speech_recognition as sr
import pyautogui
import pyttsx3
from gtts import gTTS





def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.say(text,rate-25)
    engine.runAndWait()




def getaudio():
    global recog
    recog=""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
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
    except KeyboardInterrupt:
        print("in Interrupt")
        return 0


# In[ ]:


def main():
    while True:
        text=getaudio()
        if (text!=0):
            if "enter" in text:
                pyautogui.press('enter')
            elif "backspace" in text:
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
            elif "space" in text:
                pyautogui.press('space')
            elif "stop writing" in text:
                speak("goodbye")
                break
            else:
                print(text)
                pyautogui.write(text + " ")
        


# In[ ]:



while True:
    text1 = getaudio()
    if (text1 != 0):
        if "start writing" in text1:
            speak("i am ready and listening")
            main()
