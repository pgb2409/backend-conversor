from flask import Flask, request, send_file
from flask_cors import CORS
from audio_to_musicxml import convertir_mp3_a_musicxml
import os

app = Flask(__name__)
CORS(app)

@app.route("/convertir", methods=["POST"])
def convertir():
    archivo = request.files.get("archivo")
    if not archivo:
        return "No se recibió archivo", 400

    ruta_mp3 = os.path.join("uploads", "entrada.mp3")
    archivo.save(ruta_mp3)

    ruta_xml = convertir_mp3_a_musicxml(ruta_mp3)
    return send_file(ruta_xml, mimetype="application/vnd.recordare.musicxml+xml")
