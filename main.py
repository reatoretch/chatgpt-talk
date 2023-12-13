import os
import sys
import time
import wave

import keyboard
import pyaudio
import whisper
import win32com.client

import openai

TALK_LIMIT=10
openai.api_key="YOUR_API_KEY"

class ChatGPT:
    def __init__(self):
        self.system_settings="""
        英語学習者と対話をしてもらいます。
        答えやすい質問をして、話を続けてください
        """
        self.messages=[
            {"role": "system", "content": self.system_settings}
        ]

    def conversation(self,s):
        self.messages+={"role":"user","content":s},
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )["choices"][0]["message"]
        self.messages+=response,
        return response["content"]

def speak_jp(text):
    speech = win32com.client.Dispatch("Sapi.SpVoice")
    speech.Speak(text)

def speak_en(text):
    speech = win32com.client.Dispatch("Sapi.SpVoice")
    cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
    v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Mark"]
    speech.Voice = v[0]
    speech.Speak(text)

def record_voice(out="audio.wav",seconds=5,channels=1,rate=44100):
    print("Recording start.")
    audio = pyaudio.PyAudio()
    chunk=2**10
    stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,input=True,
            input_device_index=0,
            frames_per_buffer=chunk
            )
    frames=[]
    print("Press Enter key to exit it.")
    while not keyboard.is_pressed("enter"):
      data=stream.read(chunk)
      frames.append(data)
    stream.close()
    audio.terminate()
    waveFile = wave.open(out,'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def voice_recognition(file="audio.wav"):
    model = whisper.load_model("base")
    result = model.transcribe("./audio.wav",fp16=False)
    return result["text"]

# main処理
def main():
    args = sys.argv

    if len(args)!=2:print("ex) python main.py JP|EN");exit()
    
    lang = args[1].upper()
    
    if lang == "JP":
        gpt = ChatGPT()
        for i in range(TALK_LIMIT):
            input("エンターキーを押して話します.")
            record_voice()
            s=voice_recognition()
            print("音声認識中…",s)
            s=gpt.conversation(s)
            print(s)
            speak_jp(s)
    
    elif lang == "EN":
        gpt = ChatGPT()
        for i in range(10):
            input("Press Enter to start talking.")
            record_voice()
            s=voice_recognition()
            print("Voice recognition in progress...",s)
            s=gpt.conversation(s)
            print(s)
            speak_en(s)
    
    else:
        print("Attributes is JP or EN.")

# 実行
if __name__ == "__main__":
    main()