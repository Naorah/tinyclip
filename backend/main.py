from flask import Flask, request, send_file, Response, after_this_request
from compress import compress_video_with_progress
import tempfile
import os
import subprocess
import uuid
from io import BytesIO

app = Flask(__name__)

download_map = {}

@app.route('/compress/stream', methods=['POST'])
def compress_stream():
    file = request.files.get('file')
    target_size = float(request.form.get('size'))
    speed = float(request.form.get('speed', 1.0))

    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    file.save(tmp_in.name)

    def generate():
        token = str(uuid.uuid4())
        compressed_path = tmp_in.name.replace(".mp4", "_compressed.mp4")

        # Générer la compression avec progressions
        yield from compress_video_with_progress(tmp_in.name, target_size, speed, token)

        # Stocker le token et chemin compressé pour téléchargement
        download_map[token] = {
            'compressed': compressed_path,
            'original': tmp_in.name
        }

        # Supprimer le fichier d'entrée (inutile après compression)
        try:
            os.remove(tmp_in.name)
        except:
            pass

    return Response(generate(), mimetype='text/event-stream')


@app.route('/download', methods=['GET'])
def download():
    token = request.args.get('token')
    if not token or token not in download_map:
        return "Token invalide ou expiré", 404

    entry = download_map.pop(token, None)

    if not entry:
        return "Token invalide ou expiré", 404
    
    print(entry)

    compressed_path = entry['compressed']
    original_path = entry['original']

    if not os.path.exists(compressed_path):
        return "Fichier introuvable", 404

    # Lire le fichier en mémoire
    with open(compressed_path, 'rb') as f:
        file_data = BytesIO(f.read())

    # Supprimer immédiatement le fichier du disque
    for file_path in [compressed_path, original_path]:
        try:
            os.remove(file_path)
        except:
            pass

    # Envoyer le contenu depuis la mémoire
    return send_file(
        file_data,
        mimetype='video/mp4',
        as_attachment=True,
        download_name="compressed.mp4"
    )


if __name__ == '__main__':
    app.run(debug=True, port=6465)