import whisper
import queue
import sounddevice as sd
import numpy as np

# Load Whisper model
print("[INFO] Loading Whisper model...")
model = whisper.load_model("base")

# Define trigger phrases
trigger_phrases = ["help me luna", "sos", "emergency", "save me"]

def record_audio(duration=5, samplerate=16000):
    """Record audio for a given duration."""
    print(f"[INFO] Recording audio for {duration} seconds...")
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print("[WARN] Recording status:", status)
        q.put(indata.copy())

    with sd.InputStream(callback=callback, channels=1, samplerate=samplerate):
        sd.sleep(duration * 1000)

    # Collect all recorded frames
    audio_data = []
    while not q.empty():
        audio_data.extend(q.get())

    return np.array(audio_data).flatten()

def run_voice():
    """Run continuous voice detection loop."""
    print("[VOICE MODEL] Listening for trigger phrases...")
    while True:
        try:
            # Record 5 sec audio
            audio_np = record_audio(duration=5)

            # Make sure audio is not empty
            if audio_np.size == 0:
                print("[ERROR] No audio recorded. Skipping...")
                continue

            # Transcribe using Whisper
            print("[INFO] Transcribing...")
            result = model.transcribe(audio_np, language='en')
            text = result.get("text", "").lower().strip()

            if text:
                print(f"[VOICE MODEL] Recognized: '{text}'")
            else:
                print("[VOICE MODEL] No speech detected.")

            # Check if trigger phrase is present
            if any(phrase in text for phrase in trigger_phrases):
                print("🚨 Emergency Triggered via Voice Command!")
                return "voice_detected"

        except KeyboardInterrupt:
            print("\n[INFO] Stopped by user.")
            break
        except Exception as e:
            print("[ERROR] Exception occurred:", str(e))
            continue

    return "no_voice"

if __name__ == "__main__":
    run_voice()
