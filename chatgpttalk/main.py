import os
import sys
import time
import wave

import pyaudio
import webrtcvad
import whisper
import win32com.client

from openai import OpenAI

TALK_LIMIT=10
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class ChatGpt:
    def __init__(self,lang):
        if lang=="ja":
            self.client=ChatGptJa()
        elif lang=="en":
            self.client=ChatGptEn()
        self.messages=[
            {"role": "system", "content": self.client.system_settings}
        ]
        self.system_messages = self.client.system_messages

    def conversation(self,s):
        self.messages+={"role":"user","content":s},
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        response=completion.choices[0].message
        self.messages+=response,
        return response.content

    def speak(self,text):
        self.client.speak(text)
    
    def voice_recognition(self):
        return self.client.voice_recognition()


    def record_voice(self,out="audio.wav",max_seconds=20,silence_timeout=2,channels=1,sample_rate=48000,vad_aggressiveness=3):
        audio = pyaudio.PyAudio()
        frame_duration = 30
        chunk = int(sample_rate * frame_duration / 1000)
        vad = webrtcvad.Vad(vad_aggressiveness)
        
        stream = audio.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                input_device_index=0,
                frames_per_buffer=chunk
                )
        
        frames = []
        start_time = time.time()
        last_voice_time = time.time()
        while time.time()-start_time < max_seconds:
            data=stream.read(chunk)
            if vad.is_speech(data, sample_rate):
                frames.append(data)
                last_voice_time = time.time()
            if time.time() - last_voice_time > silence_timeout:
                break
        
        stream.close()
        audio.terminate()

        waveFile = wave.open(out,'wb')
        waveFile.setnchannels(channels)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(sample_rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


class ChatGptJa:
    def __init__(self):
        self.system_settings = """
        日本語学習者と対話をしてもらいます。
        答えやすい質問をして、話を続けてください
        """
        self.system_messages = [
            "エンターキーを押して話します.",
            "音声認識中…"
        ]

    def speak(self,text):
        speech = win32com.client.Dispatch("Sapi.SpVoice")
        speech.Speak(text)
    
    def voice_recognition(self,file="audio.wav"):
        model = whisper.load_model("base")
        result = model.transcribe("./audio.wav",fp16=False,language="ja")
        return result["text"]
    

class ChatGptEn:
    def __init__(self):
        self.system_settings = """
        英語学習者と対話をしてもらいます。
        答えやすい質問をして、話を続けてください
        """
        self.system_messages = [
            "Press Enter to start talking.",
            "Voice recognition in progress..."
        ]

    def speak(self,text):
        speech = win32com.client.Dispatch("Sapi.SpVoice")
        cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
        cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
        v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Mark"]
        speech.Voice = v[0]
        speech.Speak(text)

    def voice_recognition(self,file="audio.wav"):
        model = whisper.load_model("base")
        result = model.transcribe("./audio.wav",fp16=False,language="en")
        return result["text"]
