import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser
import os
import random
import pyautogui
import psutil
import pyjokes
import requests
import json

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def set_speaking_rate(rate=180):
    engine.setProperty('rate', rate)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am assistant version 1, designed for your convenience. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, you are offline. Try again after internet is restored")
    
    return command

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')  # Replace with your email and password
        server.sendmail('your-email@gmail.com', to, content)   # Replace with sender's email
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email at the moment.")

set_speaking_rate(150)

def screenshot():
    img = pyautogui.screenshot()
    img.save(r"C:\Users\Administrator\Desktop\voicemodel with chatgpt\screenshot_{}.png".format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at " + usage + " percent")
    
    battery = psutil.sensors_battery()
    if battery is not None:
        speak(f"Battery is at {battery.percent} percent")
    else:
        speak("Battery information is not available.")

def jokes():
    speak(pyjokes.get_joke())

# Chatbot API setup
API_KEY = 'a0b67d1d95msh86ebe72a6bca11cp190a2ejsnf4cdc2582dfd'
API_HOST = 'chat-gpt26.p.rapidapi.com'

# Function to interact with the chatbot
def ask_chatbot(user_message):
    url = f'https://{API_HOST}/'
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY,
    }
    
    # Data to send to the API
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}],
    }
    
    # Sending the request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # Handling the response
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return "Sorry, I couldn't fetch a response from the chatbot."
    


# Function to close all apps on Windows
def close_all_apps():
    # Using taskkill to forcefully close all user applications
    speak("Closing all user applications.")
    print("Closing all apps...")
    # This will force close all apps opened by the user (except system processes)
    os.system("taskkill /F /FI \"USERNAME eq %USERNAME%\"")
greet()

while True:
    command = take_command()

    if "time" in command:
        tell_time()

    elif "date" in command or "day" in command:
        tell_date()

    elif 'develop' in command or 'founder' in command:
        speak("I am developed by Ananta Kadel  using ideas through youtube and udemy courses.")
        print('I am developed by Ananta Kadel using ideas through youtube and udemy courses.')

    elif 'wikipedia' in command or 'weki' in command:
        speak("Searching in Wikipedia...")
        command = command.replace("wikipedia", "")
        try:
            result = wikipedia.summary(command, sentences=2)
            print(result)
            speak(result)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results, please be more specific.")

    elif 'send email' in command or 'send mail' in command:
        try:
            speak("What would you like to say in the email?")
            content = take_command()
            if content:
                speak("Please provide the recipient's email address.")
                to = take_command()
                if to:
                    send_email(to, content)
                else:
                    speak("I didn't catch the recipient's email address.")
            else:
                speak("I didn't catch the content of the email.")
        except Exception as e:
            print(e)
            speak("Sorry, I could not send the email.")

    elif 'search on chrome' in command or 'google' in command:
        speak("What should I search for?")
        search = take_command().lower()
        if search:
            try:
                webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s').open_new_tab(f'https://www.google.com/search?q={search}')
            except webbrowser.Error:
                speak("Sorry, I couldn't open Chrome. Please check the path.")
        else:
            speak("Sorry, I didn't catch the search query.")

    elif 'logout' in command:
        os.system("shutdown -l")

    elif 'shutdown' in command:
        os.system("shutdown /s /t 1")

    elif 'restart' in command:
        os.system("shutdown /r /t 1")

    elif 'hibernate' in command:
        speak("Hibernating the system.")
        os.system("shutdown /h")

    elif 'sleep' in command:
        speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif 'play song' in command or 'play music' in command:
        songs_dir = 'C:\\Users\\Administrator\\Music'  # Use double backslashes for Windows paths
        try:
            songs = os.listdir(songs_dir)
            if songs:
                random_song = random.choice(songs)  # Select a random song
                os.startfile(os.path.join(songs_dir, random_song))  # Play the random song
                speak(f"Playing {random_song}")
            else:
                speak("No songs found in the music directory.")
        except FileNotFoundError:
            speak("Music directory not found.")

    elif 'remember that' in command:
        speak('What should I remember?')
        data = take_command()
        if data:
            speak("You asked me to remember that " + data)
            with open('data.txt', 'w') as remember:
                remember.write(data)
        else:
            speak("I didn't catch that.")

    elif 'remember anything' in command:
        try:
            with open('data.txt', 'r') as remember:
                data = remember.read()
                speak("You asked me to remember that " + data)
        except FileNotFoundError:
            speak("You haven't asked me to remember anything yet.")

    elif 'screenshot' in command:
        screenshot()
        speak("Screenshot taken.")

    elif 'cpu' in command:
        cpu()

    elif 'joke' in command:
        jokes()

    elif "gpt" in command   or "chat"  in command:
        speak("i am opening chat bot what would you like to know")
        user_message = take_command()
        if user_message:
            response = ask_chatbot(user_message)
            speak(response)

    elif "offline" in command or "stop" in command:
        speak("Thank you for giving me rest, Hope you like my service. See you again soon.")
        break
    elif "power" in command:
            close_all_apps()

    else:
        speak("I was distracted, Would you mind trying again?")
