from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from models.voice_model import detect_voice

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "Voice Backend is running"})

@app.route('/voice/detect', methods=['POST'])
def voice_detect():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file received"}), 400

    save_dir = "temp"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, audio_file.filename)
    audio_file.save(save_path)

    result = detect_voice(save_path)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
