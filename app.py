from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_name = filename.rsplit('.', 1)[0] + '.musicxml'
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    file.save(input_path)

    subprocess.run(['python', 'audio_to_musicxml.py', input_path])

    if not os.path.exists(output_path):
        return 'Conversion failed', 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
