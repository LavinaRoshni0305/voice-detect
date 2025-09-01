from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from models.voice_model import run_voice

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "Backend is running"})

@app.route('/voice/detect', methods=['POST'])
def voice_detect():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file received"}), 400

    save_path = os.path.join("temp", audio_file.filename)
    os.makedirs("temp", exist_ok=True)
    audio_file.save(save_path)

    result = run_voice(save_path)
    return jsonify({"trigger": result})

@app.route('/trigger', methods=['POST'])
def receive_trigger():
    data = request.get_json()
    source = data.get("source")
    if not source:
        return jsonify({"error": "Missing trigger source"}), 400

    print(f"[TRIGGER RECEIVED] Source: {source}")
    return jsonify({"status": "received", "source": source})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
