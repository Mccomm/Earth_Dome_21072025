import os
import uuid
import playsound
from google.cloud import texttospeech

def speak_text(text, language_code="en-US", voice_name="en-US-Studio-O"):
    # 🟡 Initialize the TTS client
    tts_client = texttospeech.TextToSpeechClient()

    # 🟡 Prepare input text
    input_text = texttospeech.SynthesisInput(text=text)

    # 🟡 Set voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # 🟡 Set audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 🟡 Synthesize speech request
    response = tts_client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    # 🟡 Create temporary folder if not exists
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    # 🟡 Save the audio to a unique temp file
    filename = os.path.join(temp_dir, f"output_{uuid.uuid4().hex}.mp3")
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    # 🔊 Play the audio
    try:
        playsound.playsound(filename)
    finally:
        os.remove(filename)  # Clean up after playback
