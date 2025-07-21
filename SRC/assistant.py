import os
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("❌ OPENAI_API_KEY not found in environment.")

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

# ✅ Function to send prompt and get response
def get_chatgpt_reply(prompt, system_prompt=""):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": str(system_prompt)},
                {"role": "user", "content": str(prompt)}
            ],
            timeout=15  # Optional timeout to avoid stalling
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return "Sorry, I'm having trouble reaching the assistant right now."
