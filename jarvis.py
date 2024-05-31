import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
# import vlc
# import pafy
from pytube import Playlist
import random
import os
import smtplib
from googleapiclient.discovery import build

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("How may i help you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f'User Said: {query}')
        return query
    except:
        print('Sorry cannot recognize please say that again')
        speak('Sorry please say that again')
        return takecommand()

# legacy
# class play_song():
#     def __init__(self):
#         # collects all urls from playlist
#         p = Playlist(
#             'https://www.youtube.com/watch?v=gvyUuxdRdR4&list=RDCLAK5uy_n9Fbdw7e6ap-98_A-8JYBmPv64v-Uaq1g&start_radio=1')
#         url_list = []
#         for url in p.video_urls:
#             url_list.append(url)

#         self.url = random.choice(url_list)
#         # get best video stream
#         self.video = pafy.new(self.url)
#         self.bestVideo = self.video.getbestvideo()
#         self.playurl = self.bestVideo.url
#         # instance created for video stream player
#         self.Instance = vlc.Instance()
#         self.player = self.Instance.media_player_new()
#         self.Media = self.Instance.media_new(self.playurl)
#         self.Media.get_mrl()
#         self.player.set_media(self.Media)
#         self.player.toggle_fullscreen()
#         # get best audio stream
#         self.audio = pafy.new(self.url)
#         self.bestAudio = self.audio.getbestaudio()
#         self.playurl2 = self.bestAudio.url
#         # instance created for audio stream player
#         self.Instance2 = vlc.Instance()
#         self.player2 = self.Instance2.media_player_new()
#         self.Media2 = self.Instance2.media_new(self.playurl2)
#         self.Media2.get_mrl()
#         self.player2.set_media(self.Media2)

#     def play(self):
#         self.player.play()
#         self.player2.play()

#     def pause(self):
#         self.player.pause()
#         self.player2.pause()

#     def stop(self):
#         self.player.stop()
#         self.player2.stop()


# # play song object created
# play_song_obj = play_song()

# Database for sendEmail function
emailDict = {'abhinav': '17122000abhinav@gmail.com',
             'aditi': '17122000abhinav@gmail.com'}


def playOnYT(query):
    api_key = os.environ.get('YOUTUBE_API')
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(part='snippet', type='video', q=query)
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    webbrowser.open(f'https://www.youtube.com/watch?v={video_id}')
    youtube.close()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    email = os.environ.get('email_id')
    password = os.environ.get('email_pass')
    server.login(email, password)
    server.sendmail(email, to, content)
    server.close()


def actions(query):
    query = str(query).lower()
    if 'wikipedia' in query:
        speak('Searching on Wikipedia..')
        query = query.replace('search', '')
        query = query.replace('on wikipedia', '')
        result = wikipedia.summary(query, sentences=3)
        speak('According to wikipedia')
        print(result)
        # set speed to 150 wpm
        engine.say(result, 150)
        engine.runAndWait()

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'youtube' in query:
        query = query.replace('on youtube', '')
        query = query.replace('search', '')
        playOnYT(query)
        # webbrowser.open(
        #     f"https://www.youtube.com/results?search_query={query}")

    elif 'open google' in query:
        webbrowser.open("google.com")

    elif 'open stackoverflow' in query:
        webbrowser.open("stackoverflow.com")

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        # set speed to 150 wpm
        print(f"\nSir the time is {strTime}")
        engine.say(f"Sir the time is {strTime}", 150)
        engine.runAndWait()

    elif 'play music' in query:
        speak('do you have a specific song in mind?')
        query = str(takecommand()).lower()
        if 'no' in query or 'any' in query or 'random' in query:
            p = Playlist(
                'https://www.youtube.com/watch?v=gvyUuxdRdR4&list=RDCLAK5uy_n9Fbdw7e6ap-98_A-8JYBmPv64v-Uaq1g&start_radio=1')
            url_list = []
            for url in p.video_urls:
                url_list.append(url)

            url = random.choice(url_list)
            webbrowser.open(url)
        else:
            query = query.replace('play', '')
            playOnYT(query)
            # play_song_obj.play()

            # elif 'stop music' in query:
            #     # play_song_obj.stop()

            # elif 'pause music' in query:
            # play_song_obj.pause()

    elif 'send email' in query:
        try:
            while True:
                speak("Please specify reciever's name")
                print("Please specify reciever's name")
                user = str(takecommand()).lower()
                if user in emailDict.keys():
                    to = emailDict[user]
                    break
                else:
                    speak("Sorry user not found")
                    print("Sorry user not found")
            while True:
                speak('what should i write?')
                print('what should i write?')
                content = takecommand()
                speak('Please confirm to send email')
                confirmation = takecommand()
                if 'yes' or 'ok' in confirmation:
                    sendEmail(to, content)
                    break
                elif 'stop' in confirmation:
                    break
            speak('Email has been sent succesfully!')
            print('Email has been sent succesfully!')
        except Exception as e:
            print(e)
            speak('Sorry Sir. Unable to send email!')

    elif query == 'sleep':
        speak('GoodBye Sir')
        os._exit(0)


print("STANDBY..")
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        query = str(query).lower()
        print(query)
        if 'henry' in query:
            wishMe()
            query = str(takecommand()).lower()
            actions(query)
    except:
        pass
