# models/voice_model.py
import whisper
import numpy as np

model = whisper.load_model("base")
trigger_phrases = ["help me luna", "sos", "emergency", "save me"]

def run_voice(audio_file_path):
    """
    Processes the uploaded audio file and checks for trigger phrases.
    """
    result = model.transcribe(audio_file_path, language='en')
    text = result['text'].lower()
    print("[VOICE MODEL] Recognized:", text)

    if any(phrase in text for phrase in trigger_phrases):
        print("🚨 Emergency Triggered via Voice Command!")
        return "voice_detected"
    return "no_voice"
