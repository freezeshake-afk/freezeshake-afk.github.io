#!/usr/bin/env python3
"""Gera clipes 9:16 falsos (enquadramento de talking head + audio com
cadencia de fala) para testar o pipeline sem gastar creditos do Flow."""
import argparse
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw


def quadro(w, h, i, n, seed):
    rng = np.random.default_rng(seed)
    im = Image.new("RGB", (w, h), (28, 30, 38))
    d = ImageDraw.Draw(im)
    for y in range(0, h, 4):                       # fundo em degrade
        t = y / h
        d.rectangle([0, y, w, y + 4],
                    fill=(int(34 + 26 * t), int(30 + 18 * t), int(44 + 30 * t)))
    cx, cy = w // 2, int(h * 0.34)                 # "cabeca" no terco superior
    r = int(w * 0.21) + int(6 * np.sin(i / 7.0))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(206, 168, 140))
    d.ellipse([cx - int(r * .34), cy - int(r * .18), cx - int(r * .12), cy + int(r * .04)],
              fill=(30, 30, 40))
    d.ellipse([cx + int(r * .12), cy - int(r * .18), cx + int(r * .34), cy + int(r * .04)],
              fill=(30, 30, 40))
    boca = int(r * (.10 + .14 * abs(np.sin(i / 2.6))))
    d.ellipse([cx - int(r * .28), cy + int(r * .34) - boca,
               cx + int(r * .28), cy + int(r * .34) + boca], fill=(96, 40, 44))
    d.rounded_rectangle([cx - int(w * .30), cy + r + int(h * .02),
                         cx + int(w * .30), h], radius=60, fill=(44, 52, 86))
    d.text((40, 40), f"CLIPE {seed:02d} / frame {i:03d}", fill=(255, 255, 255))
    return im


def audio_fala(dur, sr, seed, destino):
    rng = np.random.default_rng(seed * 7 + 1)
    n = int(dur * sr)
    t = np.arange(n) / sr
    env = np.zeros(n)
    pos = 0.0
    while pos < dur:                                # silabas de ~0.18-0.32s
        d = rng.uniform(0.16, 0.30)
        a, b = int(pos * sr), int(min(dur, pos + d) * sr)
        env[a:b] = np.hanning(max(2, b - a)) * rng.uniform(0.55, 1.0)
        pos += d + rng.uniform(0.01, 0.09)
        if rng.random() < 0.08:                     # pausa de frase
            pos += rng.uniform(0.25, 0.5)
    f0 = 118 + 14 * np.sin(2 * np.pi * 0.4 * t)
    voz = sum(np.sin(2 * np.pi * f0 * k * t) / (k * 1.7) for k in (1, 2, 3, 4))
    sinal = (voz * env + rng.normal(0, 0.012, n) * env) * 0.35
    with wave.open(destino, "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes((np.clip(sinal, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=11, help="quantidade de clipes")
    ap.add_argument("--dur", type=float, default=8.0, help="segundos por clipe")
    ap.add_argument("--w", type=int, default=720)
    ap.add_argument("--h", type=int, default=1280)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--saida", default="clipes")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    nf = int(a.dur * a.fps)
    for s in range(1, a.n + 1):
        tmp = os.path.join(a.saida, f"_tmp{s}")
        os.makedirs(tmp, exist_ok=True)
        for i in range(nf):
            quadro(a.w, a.h, i, nf, s).save(os.path.join(tmp, f"{i:04d}.png"))
        wav = os.path.join(tmp, "a.wav")
        audio_fala(a.dur, 48000, s, wav)
        dest = os.path.join(a.saida, f"flow_{s:02d}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps),
                        "-i", os.path.join(tmp, "%04d.png"), "-i", wav,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", dest],
                       check=True)
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
        print("gerado", dest)


if __name__ == "__main__":
    main()
