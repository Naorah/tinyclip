from flask import Flask, request, send_file, Response
from compress import compress_video, compress_video_with_progress
import tempfile
import os
import subprocess

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

@app.route('/compress/stream', methods=['POST'])
def compress_stream():
    file = request.files.get('file')
    target_size = float(request.form.get('size'))
    speed = float(request.form.get('speed', 1.0))

    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    file.save(tmp_in.name)

    def generate():
        yield from compress_video_with_progress(tmp_in.name, target_size, speed)

        # Nettoyage (output path est renvoyé dans le dernier message "done")
        try:
            os.remove(tmp_in.name)
            os.remove(tmp_in.name.replace(".mp4", "_compressed.mp4"))
        except:
            pass

    return Response(generate(), mimetype='text/event-stream')

@app.route('/download', methods=['GET'])
def download():
    path = request.args.get('path')
    if not path or not os.path.exists(path):
        return "Fichier introuvable", 404
    return send_file(path, as_attachment=True, download_name="compressed.mp4")


@app.route('/compress_live', methods=['POST'])
def compress_live():
    input_video = request.files['video']

    # ffmpeg: lire depuis stdin, écrire vers stdout
    command = [
        'ffmpeg',
        '-i', 'pipe:0',                 # stdin
        '-vcodec', 'libx264',
        '-crf', '28',
        '-preset', 'veryfast',
        '-f', 'mp4',
        'pipe:1'                        # stdout
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # ou tu peux capturer stderr pour les logs
    )

    # Écrit la vidéo d'entrée dans stdin et récupère stdout en réponse
    def generate():
        # Envoie le contenu au processus
        process.stdin.write(input_video.read())
        process.stdin.close()

        # Lit la sortie compressée
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            yield chunk

    return Response(
        generate(),
        mimetype='video/mp4',
        headers={"Content-Disposition": "attachment; filename=compressed.mp4"}
    )

if __name__ == '__main__':
    app.run(debug=True)