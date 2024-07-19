import speech_recognition as sr
import pyttsx3
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Stack to keep track of the current path
stack_path = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_explorer():
    try:
        current_path = os.path.expanduser("~")  # Default to the user's home directory
        stack_path.append(current_path)  # Store the current path in the stack
        os.system('explorer')  # Open File Explorer
        speak(f"file explore opened successfully. Current path stored.")
    except Exception as e:
        speak(f"Failed to open file explore: {e}")

def list_directories(path):
    try:
        entries = os.listdir(path)
        directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
        directories.sort()
        if directories:
            speak("Directories available are:")
            for i, directory in enumerate(directories, start=1):
                print(f"{i}. {directory}")
        else:
            speak("No directories found.")
        return directories
    except Exception as e:
        speak(f"Failed to list directories: {e}")
        return []

def change_directory(directory_name):
    try:
        current_path = stack_path[-1]
        new_path = os.path.join(current_path, directory_name)
        if os.path.exists(new_path) and os.path.isdir(new_path):
            stack_path.append(new_path)  # Add the new directory to the stack
            os.system(f'explorer "{new_path}"')  # Open the new directory in File Explorer
            speak(f"Changed directory to {new_path}.")
        else:
            speak("Directory not found.")
    except Exception as e:
        speak(f"Failed to change directory: {e}")

def go_back():
    try:
        if len(stack_path) > 1:
            stack_path.pop()  # Remove the current directory
            previous_path = stack_path[-1]  # Get the previous directory
            os.system(f'explorer "{previous_path}"')  # Open the previous directory in File Explorer
            speak(f"Returned to {previous_path}.")
        else:
            speak("No previous directory to go back to.")
    except Exception as e:
        speak(f"Failed to go back: {e}")

if __name__ == '__main__':
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = recognizer.listen(source)  # Recognize the audio from the source
            try:
                command = recognizer.recognize_google(audio)  # Convert audio to text
                print("You said: " + command)

                if "jarvis open explore" in command.lower():
                    open_explorer()
                elif "jarvis list directories" in command.lower():
                    # List directories in the current path
                    current_path = stack_path[-1] if stack_path else os.path.expanduser("~")
                    directories = list_directories(current_path)
                    if directories:
                        # Wait for user to specify a directory
                        speak("Please say the number of the directory you want to open.")
                        with sr.Microphone() as source:
                            audio = recognizer.listen(source)  # Recognize the audio for directory selection
                            try:
                                selection = recognizer.recognize_google(audio)
                                print(" directory no : "+selection)
                                if selection.isdigit():
                                    index = int(selection) - 1
                                    if 0 <= index < len(directories):
                                        directory_name = directories[index]
                                        change_directory(directory_name)
                                    else:
                                        speak("Invalid directory number.")
                                else:
                                    speak("Please say a valid number.")
                            except sr.UnknownValueError:
                                speak("Sorry, I didn't catch that. Please try again.")
                            except sr.RequestError as e:
                                speak("Sorry, there was an error with the speech recognition service.")
                elif "jarvis go back" in command.lower():
                    go_back()

                elif 'jarvis quit' in command.lower():
                    speak("goodby sir, have a good day")
                    engine.stop()
                    break

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                speak("Sorry, I didn't catch that. Please try again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                speak("Sorry, there was an error with the speech recognition service.")

