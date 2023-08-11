from pygame import mixer
import os
import speech_recognition as sr
import pyaudio
import wave
import time as ti
import InterfaceGPT as ChatGPT
import re
import random
from gtts import gTTS

histPreguntas = []
histRespuestas = []


def TextToVoice(text: str):
    volume = 0.7
    tts = gTTS(text, lang="es", slow=False)
    ran = random.randint(0,9999)
    filename = 'Temp' + format(ran) + '.mp3'
    tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.set_volume(volume)
    mixer.music.play()

    while mixer.music.get_busy():
        ti.sleep(0.3)

    mixer.quit()
    os.remove(filename)


def AudioToText():
    text = ""
    r = sr.Recognizer()
    with sr.AudioFile("recorded_audio.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language="es-MX")
        text = re.sub("[^A-Za-z0-9-áéíóú]+", " ", text.lower())
    return text


def promptGPT():
    prompt = ""
    for pregunta, respuesta in zip(histPreguntas, histRespuestas):
        prompt += f"el usuario pregunta:¿{pregunta}?\n"
        prompt += f"chat gpt responde:{respuesta}\n"
    return prompt


def pregunta():
    res = ""
    seconds = 5
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    CHUNK = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    timeout = ti.time() + seconds
    while True:
        if ti.time() > timeout:
            score = 0
            break
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    filename = "recorded_audio.wav"
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    res = ""
    text = ""
    text = AudioToText()
    promptChatGpt = ""
    if len(histPreguntas) > 0:
        promptChatGpt = promptGPT()
        promptChatGpt += (
            f"el usuario pregunta :¿{ text }?, dame la respuesta en español"
        )
    else:
        promptChatGpt = f"¿{ text }? , dame la respuesta en español"

    res = ChatGPT.pregunta(promptChatGpt)
    res = re.sub("[^A-Za-z0-9-áéíóú]+", " ", res.lower())
    histPreguntas.append(text)
    histRespuestas.append(res)
    TextToVoice(res)
