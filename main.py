import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Put your actual API keys here or use environment variables
newsapi = "news key here"
openai_api_key = "open api key here"

# Speak using gTTS
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Optional fallback speak method
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Use OpenAI to handle generic requests
def aiProcess(command):
    client = OpenAI(api_key=openai_api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

# Process commands
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.replace("play ", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"I couldn't find the song {song}")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        print(r.status_code)
        print(r.text)
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if not articles:
                speak("Sorry, I couldn't find any news right now.")
            else:
                for article in articles[:5]:  # Limit to 5 headlines
                    speak(f"Headline: {article['title']}")
        else:
            speak("Sorry, I couldn't fetch the news.")
    elif "exit" in c or "quit" in c:
        speak("Shutting down. Bye!")
        exit()
    else:
        output = aiProcess(c)
        speak(output)

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            print("Recognizing wake word...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                if "jarvis" in word.lower():
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
