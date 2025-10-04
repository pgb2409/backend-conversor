from flask import Flask, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # Simulación de conversión
    output_file = "resultado.musicxml"
    with open(output_file, "w") as f:
        f.write("<score-partwise version='3.1'><part><measure><note><unpitched/></note></measure></part></score-partwise>")

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
