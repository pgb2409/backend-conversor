from flask import Flask, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert():
    # Recibe el archivo MP3
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # Simulación de conversión a MusicXML
    output_file = "resultado.musicxml"
    with open(output_file, "w") as f:
        f.write("""
        <score-partwise version="3.1">
            <part>
                <measure>
                    <note>
                        <unpitched/>
                    </note>
                </measure>
            </part>
        </score-partwise>
        """)

    # Devuelve el archivo convertido
    return send_file(output_file, as_attachment=True)

# Render necesita que el servidor escuche en 0.0.0.0 y puerto 10000
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
