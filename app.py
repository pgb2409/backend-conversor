from flask import Flask, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/convertir", methods=["POST"])
def convertir():
    archivo = request.files.get("archivo")
    if not archivo:
        return "No se recibió archivo", 400

    ruta_mp3 = "entrada.mp3"
    archivo.save(ruta_mp3)

    ruta_xml = "salida.musicxml"
    with open(ruta_xml, "w") as f:
        f.write("<score-partwise version='3.1'><part><measure><note><rest/></note></measure></part></score-partwise>")

    return send_file(ruta_xml, mimetype="application/vnd.recordare.musicxml+xml")
