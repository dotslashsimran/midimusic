from flask import Flask, render_template, request, send_file, jsonify
from music.midi_generator import generate_midi_from_image
from music.audio_converter import midi_to_wav
from io import BytesIO
import base64
import os
import re
from PIL import Image
import uuid

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = 'output'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    img_data = re.sub('^data:image/.+;base64,', '', data['image'])
    img_bytes = BytesIO(base64.b64decode(img_data))
    image = Image.open(img_bytes).convert('RGB')
    image = image.resize((100, 100))

    unique_id = str(uuid.uuid4())
    midi_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{unique_id}.mid')
    wav_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{unique_id}.wav')

    notes = generate_midi_from_image(image, midi_path)
    if not notes:
        return jsonify({'error': 'No music could be generated'}), 400

    midi_to_wav(midi_path, wav_path)

    return jsonify({'audio_url': f'/output/{unique_id}.wav'})

@app.route('/output/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

@app.route('/clear', methods=['POST'])
def clear_output_folder():
    folder = app.config['OUTPUT_FOLDER']
    deleted_files = []

    for file in os.listdir(folder):
        if file.endswith(".mid") or file.endswith(".wav"):
            file_path = os.path.join(folder, file)
            try:
                os.remove(file_path)
                deleted_files.append(file)
            except Exception as e:
                print(f"Error deleting {file}: {e}")

    return jsonify({"deleted": deleted_files})

if __name__ == '__main__':
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)