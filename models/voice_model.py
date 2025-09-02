import whisper
import os

# Load model once at startup
model = whisper.load_model("base")

# Define trigger phrases
trigger_phrases = ["help", "emergency", "sos", "save me"]

def detect_voice(audio_path):
    """
    Transcribe audio and check for emergency phrases.
    """
    if not os.path.exists(audio_path):
        return {"triggered": False, "error": "File not found"}

    result = model.transcribe(audio_path)
    text = result["text"].lower()

    if any(phrase in text for phrase in trigger_phrases):
        return {"triggered": True, "transcript": text}
    return {"triggered": False, "transcript": text}
