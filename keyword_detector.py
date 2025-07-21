import sounddevice as sd
import numpy as np
import queue
import vosk
import json
import os

# Load Vosk model once
model_path = os.path.join("models", "vosk-model-en-us-0.22")
model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def wait_for_keyword(keywords=["hello earth dome", "yes"]):
    print("🎙️ Listening for wake word...")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if any(kw in text for kw in keywords):
                    print(f"🗣️ You said: {text}")
                    return text
