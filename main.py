import os
import time
import subprocess
from dotenv import load_dotenv

from SRC.microphone import listen_to_microphone
from SRC.language_profile import get_language_profile
from SRC.assistant import get_chatgpt_reply
from SRC.tts import speak_text

# === Load .env and TTS credentials ===
load_dotenv()

# Get the path to the credentials JSON file from the .env file
GOOGLE_TTS_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not GOOGLE_TTS_CREDENTIALS or not os.path.exists(GOOGLE_TTS_CREDENTIALS):
    raise EnvironmentError("❌ GOOGLE_TTS_CREDENTIALS not found or file does not exist.")

# Set the environment variable so Google Cloud SDK can authenticate
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_CREDENTIALS



# === Fallback for off-topic questions ===
OFF_TOPIC_RESPONSE = "I’m here to guide you through the Earth Dome and its context. Would you like to hear more about that?"

# === Messages ===
AUTO_MESSAGES = [
    "Welcome! You’re experiencing the Earth Dome installation, a space that represents a blend of tradition and innovation. "
    "It symbolizes Qatar’s deep connection to its land, culture, and architectural heritage. The first Earth Dome was commissioned "
    "by His Highness Sheikh Khalifa bin Hamad Al Thani, the father Emir, and today it is reimagined by Qatar Museums as a way to honor the nation’s legacy through art, architecture, and collective memory.",
    
    "Rather than importing new ideas, the Earth Dome asked: What can the land already teach us? The answer was stabilized earth—a humble yet intelligent material formed by mixing local soil with cement to enhance strength and durability."
    "This wasn’t merely about structure. It was philosophy made tangible: using what is underfoot to build what stands above."
    "The material reflected the ethos of self-sufficiency, low-carbon living, and thermal performance—long before those terms became global design priorities..",
    
    "The design of the Earth Dome wasn’t arbitrary—it was an architectural response to extreme conditions."
    "Thick earth walls provided thermal mass, keeping the interior cool during scorching days and warm during desert nights. Its circular form and domed roof promoted natural convection, allowing hot air to rise and escape."
    "These passive systems reduced the need for artificial cooling, proving that traditional intelligence could outperform modern excess. It became a living lab for climate-adaptive design in the Gulf..",
    
    "More than a structure, the Earth Dome was a functional prototype—a test of ideas that could shape Qatar’s future."
    "Researchers, architects, and policymakers studied it not as an object, but as a process. Could these techniques be scaled? Could other materials behave similarly?"
    "The Dome became a seed from which a whole school of thought could grow—one focused on vernacular modernism: a blend of cultural relevance, structural logic, and environmental care..",

    "Today, the Earth Dome has been reimagined—not just rebuilt, but reborn. This installation honors the past and the visionary who first commissioned it."
    "Built from lightweight metal and lined with high-performance insulation like aerogel—known for its ultra-low thermal conductivity—it combines function and symbolism."
    "It’s a reminder that a single act of vision can ripple across generations, shaping what innovation looks like in our time.."

]

AUTO_RESPONSES = {
    "Would you like to hear the story behind it?": "It’s a fascinating story. Let’s begin the Earth Dome journey."
}

VIDEO_PATH = os.path.join(os.getcwd(), "data", "earth_dome_video.mp4")

# === Video Playback ===
def play_video():
    try:
        print("🎬 Playing Earth Dome video...")
        if os.name == "nt":
            os.startfile(VIDEO_PATH)
        else:
            subprocess.call(["open", VIDEO_PATH])
    except Exception as e:
        print(f"❌ Error playing video: {e}")

# === Main Program ===
if __name__ == "__main__":
    print("🔊 Earth Dome Assistant is now listening...")

    last_auto_time = time.time()
    auto_index = 0
    played_video = False

    try:
        while True:
            current_time = time.time()

            # === Step 1: After 60s, play the video once ===
            if not played_video and current_time - last_auto_time >= 60:
                play_video()
                time.sleep(45)  # Wait for video to complete
                played_video = True
                last_auto_time = time.time()
                auto_index = 1  # Move to next message
                continue

            # === Step 2: Play remaining auto messages every 60s ===
            if played_video and auto_index < len(AUTO_MESSAGES) and current_time - last_auto_time >= 60:
                speak_text(AUTO_MESSAGES[auto_index], language_code="en-US", voice_name="en-US-Studio-O")
                last_auto_time = time.time()
                auto_index += 1
                continue

            # === Step 3: Restart cycle after last message ===
            if auto_index == len(AUTO_MESSAGES):
                print("⏳ Waiting 180 seconds before restarting auto-messages...")
                time.sleep(180)
                auto_index = 0
                played_video = False
                last_auto_time = time.time()
                continue

            # === Step 4: Listen for user input ===
            question = listen_to_microphone()
            if question:
                if "stop" in question.lower():
                    print("🛑 Exiting system...")
                    break

                # === Affirmative response to AUTO_RESPONSES ===
                agreement_keywords = ["yes", "yeah", "sure", "go ahead", "okay", "alright"]
                if any(word in question.lower() for word in agreement_keywords):
                    for key_phrase, response in AUTO_RESPONSES.items():
                        if key_phrase in AUTO_MESSAGES[0]:
                            print(f"🤖 Auto Response: {response}")
                            speak_text(response, language_code="en-US", voice_name="en-US-Studio-O")
                            break
                    continue

                # === Process GPT response ===
                profile = get_language_profile(question)
                reply = get_chatgpt_reply(question, system_prompt=profile)
                print(f"💬 ChatGPT: {reply}")
                speak_text(reply, language_code="en-US", voice_name="en-US-Studio-O")

    except KeyboardInterrupt:
        print("\n👋 Assistant terminated by user.")
