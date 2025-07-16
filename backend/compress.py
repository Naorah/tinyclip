import os
import subprocess
from pathlib import Path
import time

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
    speed: float = 1.0,
    output_token: str = None
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
        yield f"event: done\ndata: {output_token}\n\n"
    else:
        yield f"event: error\ndata: Compression échouée\n\n"