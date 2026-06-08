from dotenv import load_dotenv
from sarvamai import SarvamAI
import os

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)




response = client.speech_to_text.transcribe(
    file=open("Conference.wav", "rb"),
    model="saaras:v3",
    mode="transcribe",  # or "translate", "verbatim", "translit", "codemix"
)

print(response)
