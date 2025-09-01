import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# You can later load these from user settings or database
trigger_phrases = ["help me luna", "sos", "emergency", "save me"]

def run_voice(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            text = response["text"].lower()
            print("[VOICE API] Transcribed:", text)

            if any(phrase in text for phrase in trigger_phrases):
                print("🚨 Emergency Triggered via Voice Command!")
                return "voice_detected"
            return "no_voice"
    except Exception as e:
        print("[VOICE API] Error:", str(e))
        return "error"
