import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import os
import pyautogui
import subprocess

# 1. Voice Engine Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 
engine.setProperty('rate', 180) 

def speak(text):
    print(f"Nova: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. Listening Logic
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n--- Listening ---")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("--- Recognizing ---")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        return "none"
    return query.lower()

# 3. Main Loop with ALL Commands
if __name__ == "__main__":
    speak("Hey user! I am Nova. How can I help?")
    
    while True:
        query = take_command()

        # --- WEATHER ---
        if 'weather' in query:
            speak("Checking the local forecast for you now.")
            webbrowser.open("https://www.google.com/search?q=weather+near+me")

        # --- MAPS ---
        elif 'where is' in query or 'map of' in query:
            location = query.replace("where is", "").replace("map of", "").strip()
            speak(f"Locating {location} on Google Maps.")
            webbrowser.open(f"https://www.google.com/maps/search/{location}")

        # --- PLAY (YouTube) ---
        elif 'play' in query:
            song = query.replace("play", "").strip()
            speak(f"Finding {song} on YouTube. Enjoy!")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        # --- TIME ---
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"It is currently {strTime}")

        # --- WIKIPEDIA ---
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                speak(results)
            except:
                speak("I couldn't find a clear match for that.")

        # --- CAMERA ---
        elif 'open camera' in query:
            speak("Opening your camera now.")
            subprocess.run('start microsoft.windows.camera:', shell=True)

        # --- SCREENSHOT ---
        elif 'screenshot' in query:
            speak("Taking a screenshot. Check your desktop!")
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
                local = os.path.join(os.path.expanduser("~"), "Desktop")
                path = os.path.join(onedrive if os.path.exists(onedrive) else local, filename)
                pyautogui.screenshot(path)
                speak("Screenshot saved.")
            except:
                speak("Error saving screenshot.")

        # --- WEB SITES ---
        elif 'open youtube' in query:
            speak("Opening YouTube.")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("google.com")

        # --- SEARCH ---
        elif 'search' in query:
            search_item = query.replace("search", "").strip()
            speak(f"Searching Google for {search_item}.")
            webbrowser.open(f"https://www.google.com/search?q={search_item}")

        # --- EXIT ---
        elif 'stop' in query or 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a great day.")
            break