"""Da tempo a cada palavra do roteiro.

1) faster-whisper (preferido): timestamps reais da fala.
2) fallback: distribuicao por energia do audio (sem rede, sem modelo).
"""
import difflib
import re
import subprocess
import unicodedata
import wave

import numpy as np


def _norm(p):
    p = unicodedata.normalize("NFKD", p.lower())
    p = "".join(c for c in p if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", p)


def _silabas(p):
    g = re.findall(r"[aeiouyáâãàéêíóôõúü]+", p.lower())
    return max(1, len(g))


# ---------------------------------------------------------------- whisper

def whisper_palavras(wav, modelo="small", idioma="pt"):
    from faster_whisper import WhisperModel
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language=idioma, word_timestamps=True, vad_filter=True)
    out = []
    for s in segs:
        for w in (s.words or []):
            if w.word.strip():
                out.append({"w": w.word.strip(), "s": float(w.start), "e": float(w.end)})
    return out


# ---------------------------------------------------------------- energia

def envelope(wav, hz=100):
    with wave.open(wav, "rb") as f:
        sr, n = f.getframerate(), f.getnframes()
        a = np.frombuffer(f.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    salto = max(1, sr // hz)
    corte = len(a) - len(a) % salto
    quadros = a[:corte].reshape(-1, salto)
    return np.sqrt((quadros ** 2).mean(1) + 1e-12), hz


def energia_palavras(wav, palavras):
    """Distribui as palavras do roteiro sobre a energia da fala."""
    rms, hz = envelope(wav)
    dur = len(rms) / hz
    db = 20 * np.log10(rms + 1e-9)
    limiar = np.percentile(db, 55) - 6
    fala = db > limiar
    peso = np.where(fala, rms, 0.0)
    if peso.sum() <= 0:
        peso = np.ones_like(rms)
    acum = np.cumsum(peso) / peso.sum()

    silabas = np.array([_silabas(p) for p in palavras], dtype=float)
    alvo = np.cumsum(silabas) / silabas.sum()

    bordas = np.interp(np.concatenate([[0.0], alvo]), acum, np.arange(len(acum)) / hz)
    bordas[0], bordas[-1] = 0.0, dur
    return [{"w": p, "s": float(bordas[i]), "e": float(bordas[i + 1])}
            for i, p in enumerate(palavras)]


# ---------------------------------------------------------------- casamento

def casar(palavras_roteiro, palavras_audio):
    """Casa o roteiro com o que o whisper ouviu; devolve palavras com tempo
    e o mapa indice_roteiro -> tempo (para posicionar os marcadores)."""
    a = [_norm(p) for p in palavras_roteiro]
    b = [_norm(w["w"]) for w in palavras_audio]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)

    saida = [None] * len(palavras_roteiro)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            saida[i + k] = {"w": palavras_roteiro[i + k],
                            "s": palavras_audio[j + k]["s"],
                            "e": palavras_audio[j + k]["e"]}

    # interpola os buracos (palavras do roteiro que o whisper nao pegou)
    conhecidos = [i for i, v in enumerate(saida) if v]
    if not conhecidos:
        return energia_palavras_fallback(palavras_roteiro, palavras_audio)
    for i, v in enumerate(saida):
        if v:
            continue
        ant = max([k for k in conhecidos if k < i], default=None)
        pos = min([k for k in conhecidos if k > i], default=None)
        t0 = saida[ant]["e"] if ant is not None else palavras_audio[0]["s"]
        t1 = saida[pos]["s"] if pos is not None else palavras_audio[-1]["e"]
        vazios = [k for k in range(i, len(saida)) if not saida[k]
                  and (pos is None or k < pos)]
        passo = (t1 - t0) / max(1, len(vazios))
        for n_, k in enumerate(vazios):
            saida[k] = {"w": palavras_roteiro[k], "s": t0 + n_ * passo,
                        "e": t0 + (n_ + 1) * passo}
    return saida


def energia_palavras_fallback(palavras_roteiro, palavras_audio):
    dur = palavras_audio[-1]["e"] if palavras_audio else 1.0
    passo = dur / max(1, len(palavras_roteiro))
    return [{"w": p, "s": i * passo, "e": (i + 1) * passo}
            for i, p in enumerate(palavras_roteiro)]


# ---------------------------------------------------------------- api

def alinhar(wav, palavras_roteiro, usar_whisper=True, modelo="small", idioma="pt"):
    modo = "energia"
    if usar_whisper:
        try:
            ouvidas = whisper_palavras(wav, modelo, idioma)
            if ouvidas:
                return casar(palavras_roteiro, ouvidas), "whisper"
        except Exception as e:                                  # noqa: BLE001
            print(f"  [aviso] whisper indisponivel ({type(e).__name__}); "
                  f"usando alinhamento por energia.")
    return energia_palavras(wav, palavras_roteiro), modo


def extrair_wav(video, destino, sr=16000):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1",
                    "-ar", str(sr), "-c:a", "pcm_s16le", destino], check=True)
    return destino
