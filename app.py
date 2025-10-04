import os
from flask import Flask, request, jsonify
from flask_cors import CORS # <--- NUEVA IMPORTACIÓN
from werkzeug.utils import secure_filename
from audio_to_musicxml import generate_drum_score

app = Flask(__name__)

# Aplicar CORS a toda la aplicación
CORS(app) # <--- NUEVA LÍNEA CLAVE PARA PERMITIR LA COMUNICACIÓN FRONTEND/BACKEND

# Configuración: Permitir solo archivos MP3 y definir ruta temporal
ALLOWED_EXTENSIONS = {'mp3'}
UPLOAD_FOLDER = '/tmp/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convertir', methods=['POST'])
def convertir():
    # Verificar si el archivo está en la petición
    if 'mp3File' not in request.files:
        return jsonify({'error': 'No se encontró el archivo MP3.'}), 400

    file = request.files['mp3File']

    # Si el usuario no selecciona un archivo
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar el archivo temporalmente
        file.save(temp_path)

        try:
            # Llama a la función de generación de partitura (ahora con XML válido)
            xml_content = generate_drum_score(temp_path)
            
            # Limpiar el archivo subido después de usarlo
            os.remove(temp_path)
            
            # Devuelve el contenido XML como texto
            return xml_content, 200, {'Content-Type': 'application/xml'}

        except Exception as e:
            # Manejo de errores durante la conversión
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({'error': f'Error durante el procesamiento del archivo: {str(e)}'}), 500

    return jsonify({'error': 'Tipo de archivo no permitido.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
