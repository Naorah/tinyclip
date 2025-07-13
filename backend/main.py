from flask import Flask, request, send_file
from compress import compress_video
import tempfile
import os

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files.get('file')
    target_size = float(request.form.get('size'))
    speed = float(request.form.get('speed', 1.0))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_in:
        file.save(tmp_in.name)
        output_path = compress_video(tmp_in.name, target_size, speed)

    # Retourner le fichier compressé en téléchargement
    response = send_file(output_path, as_attachment=True, download_name="compressed.mp4")

    # Nettoyage des fichiers temporaires après envoi
    try:
        os.remove(tmp_in.name)
        os.remove(output_path)
        # Supprimer aussi les logs de ffmpeg (.log, .log.mbtree, etc.) si nécessaire
    except Exception:
        pass

    return response

if __name__ == '__main__':
    app.run(debug=True)