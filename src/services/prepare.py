# src/services/prepare.py
import subprocess
from pathlib import Path
from models.video import VideoAsset

def run_ffmpeg(cmd: list[str]):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)

def prepare_asset(src: Path, out: Path, vertical: bool = True, max_length: int = 60) -> VideoAsset:
    out.parent.mkdir(parents=True, exist_ok=True)
    # Простейшая нормализация под 1080x1920, жёсткая обрезка по длине
    vf = []
    if vertical:
        vf.append("scale=1080:1920:force_original_aspect_ratio=decrease")
        vf.append("pad=1080:1920:(ow-iw)/2:(oh-ih)/2")
    vf_chain = ",".join(vf) if vf else "null"
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-t", str(max_length),
        "-vf", vf_chain,
        "-r", "30",
        "-c:v", "libx264", "-b:v", "3000k",
        "-c:a", "aac", "-b:a", "128k",
        str(out)
    ]
    run_ffmpeg(cmd)
    return VideoAsset(src_path=str(src), prepared_path=str(out))