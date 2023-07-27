import pygame
import os
import speech_recognition as sr
from dotenv import load_dotenv
import openai
import pyaudio
import wave
import time
import InterfaceGPT as ChatGPT
from datetime import datetime, timedelta
import re



histPreguntas=[]
histRespuestas=[]

def TextToVoice(text:str):
    voice = 'es-GT-AndresNeural'
    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "data.mp3"'
    os.system(command)
    pygame.init()
    pygame.mixer.init()
    f=open('data.mp3')
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()

def AudioToText():
    text=''
    r = sr.Recognizer()
    with sr.AudioFile('recorded_audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language = "es-MX")
        text=re.sub('[^A-Za-z0-9-áéíóú]+', ' ', text.lower())
    return text

def promptGPT(): 
    prompt=''
    for pregunta,respuesta in zip(histPreguntas,histRespuestas):
        prompt+=f'el usuario pregunta:¿{pregunta}?\n'
        prompt+=f'chat gpt responde:{respuesta}\n'
    return prompt

def pregunta():
    res=''
    seconds=5
    FORMAT = pyaudio.paInt16  
    CHANNELS = 2
    RATE = 48000  
    CHUNK = 1024  
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames=[]
    timeout = time.time() + seconds
    while True:
        if time.time() > timeout:
           score=0
           break
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    filename = "recorded_audio.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    res=''
    text=''
    text=AudioToText() 
    promptChatGpt=''
    if len(histPreguntas) >0:
        promptChatGpt=promptGPT()
        promptChatGpt+=f'el usuario pregunta :¿{ text }?, dame la respuesta en español'
    else:
        promptChatGpt=f'¿{ text }? , dame la respuesta en español'

    res=ChatGPT.pregunta(promptChatGpt) 
    res=re.sub('[^A-Za-z0-9-áéíóú]+', ' ', res.lower())
    histPreguntas.append(text)
    histRespuestas.append(res)
    TextToVoice(res)
    




