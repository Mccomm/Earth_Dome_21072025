import speech_recognition as sr

def detect_audio_keyword(trigger_phrase="hello earth dome"):
    """
    Listens through the microphone and returns True if the trigger phrase is heard.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for wake word...")
        try:
            audio = recognizer.listen(source, phrase_time_limit=4)
            text = recognizer.recognize_google(audio)
            print(f"👂 Heard: {text}")
            return trigger_phrase.lower() in text.lower()
        except sr.UnknownValueError:
            print("🤫 Didn't catch that.")
            return False
        except sr.RequestError as e:
            print(f"⚠️ API error: {e}")
            return False
