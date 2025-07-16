import os
import subprocess
from pathlib import Path
import time

def compress_video(input_video: str, target_size_mb: float, speed: float = 1.0) -> str:
    """
    Compresse une vidéo pour atteindre une taille cible en Mo et ajuste sa vitesse
    
    Args:
        input_video: Chemin de la vidéo d'entrée
        target_size_mb: Taille cible en Mo
        speed: Facteur de vitesse (>1 pour accélérer)
        
    Returns:
        Chemin de la vidéo compressée
    """
    # Vérifier que le fichier existe
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Le fichier {input_video} n'existe pas")
        
    # Vérifier que la vitesse est valide
    if speed <= 0:
        raise ValueError("La vitesse doit être supérieure à 0")
        
    # Obtenir la durée de la vidéo en secondes
    duration = float(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', input_video
    ]).decode('utf-8').strip())
    
    # Calculer le bitrate cible (en bits/s) pour atteindre la taille souhaitée
    target_size_bits = target_size_mb * 8 * 1024 * 1024
    target_bitrate = int(target_size_bits / duration)
    
    # Préparer le nom du fichier de sortie
    input_path = Path(input_video)
    output_video = str(input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}")
    
    # Paramètre de vitesse pour ffmpeg
    speed_param = f"setpts={1/speed}*PTS[v];asetrate=44100*{speed}[a]" if speed != 1 else None
    
    # Compresser la vidéo avec ffmpeg
    base_command = [
        'ffmpeg', '-i', input_video,
        '-c:v', 'libx264',
        '-b:v', f'{target_bitrate}',
        '-vsync', '2'  # Ajout de vsync pour gérer les timestamps
    ]
    
    if speed_param:
        base_command.extend(['-filter_complex', speed_param, '-map', '[v]', '-map', '[a]'])
    
    # Premier passage
    first_pass = base_command + ['-pass', '1', '-f', 'null', '/dev/null']
    subprocess.run(first_pass)
    
    # Second passage
    second_pass = base_command + ['-pass', '2', output_video]
    subprocess.run(second_pass)
    
    return output_video

def parse_ffmpeg_progress_line(line: str) -> dict:
    """Parses a line of ffmpeg stderr and extracts useful info."""
    if "time=" not in line:
        return {}
    try:
        tokens = dict(item.split('=') for item in line.strip().split() if '=' in item)
        if 'time' in tokens:
            h, m, s = map(float, tokens['time'].split(':'))
            current_time = h * 3600 + m * 60 + s
            tokens['time_seconds'] = current_time
        return tokens
    except:
        return {}


def compress_video_with_progress(
    input_video: str,
    target_size_mb: float,
    speed: float = 1.0
):
    """Yields ffmpeg progress in SSE format during compression."""
    if not os.path.exists(input_video):
        yield f"event: error\ndata: Le fichier {input_video} n'existe pas\n\n"
        return

    if speed <= 0:
        yield f"event: error\ndata: La vitesse doit être supérieure à 0\n\n"
        return

    duration = float(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', input_video
    ]).decode().strip())

    target_size_bits = target_size_mb * 8 * 1024 * 1024
    target_bitrate = int(target_size_bits / duration)

    input_path = Path(input_video)
    output_video = str(input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}")

    base_cmd = [
        'ffmpeg', '-y', '-i', input_video,
        '-c:v', 'libx264',
        '-b:v', f'{target_bitrate}',
        '-vsync', '2',
        '-pass', '2',
        output_video
    ]

    if speed != 1:
        speed_filter = f"setpts={1/speed}*PTS[v];asetrate=44100*{speed}[a]"
        base_cmd = [
            'ffmpeg', '-y', '-i', input_video,
            '-filter_complex', speed_filter,
            '-map', '[v]', '-map', '[a]',
            '-c:v', 'libx264',
            '-b:v', f'{target_bitrate}',
            '-vsync', '2',
            '-pass', '2',
            output_video
        ]

    # Start subprocess
    process = subprocess.Popen(
        base_cmd,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    start = time.time()

    for line in process.stderr:
        progress = parse_ffmpeg_progress_line(line)
        if not progress:
            continue

        t = progress.get("time_seconds", 0)
        percent = (t / duration) * 100
        elapsed = time.time() - start
        eta = max(0, (elapsed / percent) * (100 - percent)) if percent > 0 else 0

        yield (
            f"event: progress\n"
            f"data: {{" +
            f"\"percent\": {percent:.2f}, \"eta\": {eta:.1f}" +
            f"}}\n\n"
        )

    process.wait()

    if process.returncode == 0:
        yield f"event: done\ndata: {output_video}\n\n"
    else:
        yield f"event: error\ndata: Compression échouée\n\n"