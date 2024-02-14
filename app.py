from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

@app.route('/')
def index():
    return "Welcome to the audio transcription API!"

@app.route('/audio/audio_transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file.save("uploaded_audio.wav")  # Save the file to disk
        transcription_result = query("uploaded_audio.wav")
        return jsonify(transcription_result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
