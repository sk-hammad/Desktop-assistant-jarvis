import webbrowser # for websites
import speech_recognition as sr
import pyttsx3
import os
import pyautogui # screenshot
import datetime
import subprocess # for browser
import openai

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set your OpenAI API key

def speak(text): # electronic voice
    engine.say(text)
    engine.runAndWait()

def calculator():
    try:
        os.system('calc') # command to open the calculator
        speak("Calculator opened successfully.")
    except Exception as e:
        speak(f"Failed to open the calculator: {e}")

def take_screenshot():
    try:
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.png") # name of screenshot
        save_path = os.path.join("C:\\Users\\Hammad\\OneDrive\\Pictures\\Screenshots", filename) # path to store the screenshot
        screenshot = pyautogui.screenshot() # this will take screenshot
        screenshot.save(save_path) # save the screenshot
        os.startfile(save_path) # display the screenshot
        speak(f"Screenshot taken and stored as {filename}.")
    except Exception as e:
        speak(f"Failed to take screenshot: {e}")

def open_brave():
    try:
        subprocess.Popen(['C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'])
        speak("Brave browser opened successfully.")
    except Exception as e:
        speak(f"Failed to open Brave browser: {e}")



# Infinite loop to keep the assistant running
if __name__ == '__main__':
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source) # recognize the audio from the source
            try:
                command = recognizer.recognize_google(audio) # this will convert audio to text
                print("You said: " + command)

                sites = [
                    ['youtube', "https://www.youtube.com/"],
                    ["leetcode 1", "https://leetcode.com/problemset/"],
                    ["leetcode 2", "https://leetcode.com/problemset/"],
                    ["my personal gmail", "https://mail.google.com/mail/u/2/#inbox"],
                    ["another gmail", "https://mail.google.com/mail/u/0/#inbox"]
                ]

                for site in sites:
                    if f"jarvis open {site[0]}".lower() in command.lower():
                        try:
                            speak(f"Opening {site[0]}")
                            webbrowser.open(site[1])
                            speak(f"{site[0]} opened successfully.")
                        except Exception as e:
                            speak(f"Failed to open {site[0]}: {e}")

                if "hey jarvis" in command.lower():
                    speak("Hello, sir")
                elif "jarvis open calculator" in command.lower():
                    speak("Opening calculator")
                    calculator()
                elif "jarvis take screenshot" in command.lower():
                    speak('Taking screenshot')
                    take_screenshot()
                elif "jarvis open brave" in command.lower():
                    speak("Opening Brave")
                    open_brave()
                elif "jarvis quit" in command.lower():
                    speak("goodby sir, have a good day")
                    engine.stop()
                    break


            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
