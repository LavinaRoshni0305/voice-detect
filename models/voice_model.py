from faster_whisper import WhisperModel
import numpy as np
import soundfile as sf

# Load the model once
model_size = "small"  # or "base", "medium" (larger = more accurate)
model = WhisperModel(model_size)

# Emergency trigger phrases
trigger_phrases = ["help me luna", "sos", "emergency", "save me"]

def detect_voice(file_path):
    audio, samplerate = sf.read(file_path)
    segments, info = model.transcribe(audio, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text.lower() + " "
    
    print("[VOICE MODEL] Recognized:", text)
    
    if any(phrase in text for phrase in trigger_phrases):
        print("🚨 Emergency Triggered via Voice Command!")
        return "voice_detected"
    return "no_voice"
