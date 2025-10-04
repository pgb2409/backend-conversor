from flask import Flask, request, send_file
from audio_to_musicxml import convertir_mp3_a_musicxml
import os

app = Flask(__name__)
UPLOAD_FOLDER = "cargas"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convertir", methods=["POST"])
def convertir():
    archivo = request.files.get("archivo")
    if not archivo:
        return "No se recibió archivo", 400

    ruta_mp3 = os.path.join(UPLOAD_FOLDER, "temp.mp3")
    ruta_xml = os.path.join(UPLOAD_FOLDER, "partitura.musicxml")

    archivo.save(ruta_mp3)
    convertir_mp3_a_musicxml(ruta_mp3, ruta_xml)

    return send_file(ruta_xml, as_attachment=True)
