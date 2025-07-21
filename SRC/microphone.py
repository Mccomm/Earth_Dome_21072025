import speech_recognition as sr

def listen_to_microphone(timeout=5, phrase_time_limit=10, language="en-US"):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = recognizer.recognize_google(audio, language=language)
                print(f"🗣️ You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("⏱️ Timeout: No speech detected.")
                return None
            except sr.UnknownValueError:
                print("🙉 Sorry, I couldn't understand that.")
                return None
            except sr.RequestError:
                print("🚫 Speech recognition service error.")
                return None

    except (AttributeError, OSError) as e:
        print("⚠️ Microphone not available or PyAudio not installed.")
        return fallback_input()


def fallback_input():
    try:
        return input("⌨️ Enter your message instead: ")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
