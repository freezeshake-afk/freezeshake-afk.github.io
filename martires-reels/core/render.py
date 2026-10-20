"""Monta o reel com ffmpeg: concat dos clipes, modo cheio x board,
PiP arredondado, overlays animados, legendas e trilha com ducking."""
import json
import os
import subprocess

from . import artes


def _exec(cmd, descr=""):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou {descr}:\n{r.stderr[-2500:]}")
    return r


def duracao(caminho):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", caminho], capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def tem_audio(caminho):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=index", "-of", "json", caminho],
                       capture_output=True, text=True, check=True)
    return bool(json.loads(r.stdout).get("streams"))


# ---------------------------------------------------------------- concat

def juntar_clipes(clipes, tema, destino, crossfade=0.0):
    """Normaliza e concatena os clipes do Flow em um unico arquivo 9:16."""
    s = tema["saida"]
    w, h, fps = s["w"], s["h"], s["fps"]
    escala = (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h},setsar=1,fps={fps},format=yuv420p")

    entradas, filtros, vlab, alab = [], [], [], []
    for i, c in enumerate(clipes):
        entradas += ["-i", c]
        filtros.append(f"[{i}:v]{escala}[v{i}]")
        vlab.append(f"[v{i}]")
        if tem_audio(c):
            filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        else:
            filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{duracao(c)}[a{i}]")
        alab.append(f"[a{i}]")

    filtros.append("".join(v + a for v, a in zip(vlab, alab)) +
                   f"concat=n={len(clipes)}:v=1:a=1[vo][ao]")
    _exec(["ffmpeg", "-v", "error", "-y", *entradas,
           "-filter_complex", ";".join(filtros), "-map", "[vo]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-c:a", "aac", "-b:a", "256k", destino], "no concat dos clipes")
    return destino


# ---------------------------------------------------------------- timeline

def _uniao(intervalos):
    return "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in intervalos)


def montar(fala, tema, saida, intervalos_board, overlays, legendas_ass,
           musica=None, trilha_volume=None, zoom_lento=False, log=print):
    """
    fala              : video unico ja concatenado (voz + imagem do clone)
    intervalos_board  : [(t0,t1)] em que entra o modo board
    overlays          : [{'png','t0','t1','x','y','slide'}]
    """
    s, p, an = tema["saida"], tema["pip"], tema["animacao"]
    W, H, FPS = s["w"], s["h"], s["fps"]
    dur = duracao(fala)
    tmp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "build", "_arte")
    os.makedirs(tmp, exist_ok=True)

    f_fundo = artes.fundo(tema, os.path.join(tmp, "fundo.png"))
    f_mold = artes.moldura_pip(tema, os.path.join(tmp, "moldura.png"))
    f_mask = artes.mascara_pip(tema, os.path.join(tmp, "mask.png"))
    cx, cy, cw, ch = artes._geo_pip(tema)

    def img(caminho):
        """PNG como stream continuo: sem o loop a imagem tem 1 frame so,
        o fade/alpha congela em t=0 e o overlay some."""
        return ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", caminho]

    entradas = ["-i", fala, *img(f_fundo), *img(f_mold), *img(f_mask)]
    base_n = 4
    for o in overlays:
        entradas += img(o["png"])

    F = []
    # --- modo cheio -------------------------------------------------
    cheio = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
             f"crop={W}:{H},setsar=1,fps={FPS}")
    if zoom_lento:
        cheio += (f",zoompan=z='min(zoom+0.00018,1.08)':d=1:"
                  f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}")
    F.append(cheio + "[cheio]")

    if intervalos_board:
        # --- PiP: recorte focado no rosto, cantos arredondados ------
        ar = cw / ch
        z = max(1.0, float(p.get("zoom", 1.0)))
        rec_w = int(W / z) // 2 * 2
        rec_h = int(rec_w / ar) // 2 * 2
        off_x = (W - rec_w) // 2 // 2 * 2
        off_y = max(0, int((H - rec_h) * p["crop_foco_y"])) // 2 * 2
        F.append(f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"setsar=1,fps={FPS},crop={rec_w}:{rec_h}:{off_x}:{off_y},"
                 f"scale={cw}:{ch},format=rgba[pipc]")
        F.append(f"[3:v]scale={cw}:{ch},format=gray[pipm]")
        F.append("[pipc][pipm]alphamerge[pip]")
        F.append(f"[1:v]scale={W}:{H},format=rgba[bg]")
        F.append(f"[bg][pip]overlay={cx}:{cy}:format=auto[bg2]")
        F.append(f"[2:v]scale={W}:{H},format=rgba[mold]")
        F.append("[bg2][mold]overlay=0:0:format=auto,format=yuv420p[board]")
        F.append(f"[cheio][board]overlay=0:0:enable='{_uniao(intervalos_board)}'[base]")
    else:
        F.append("[cheio]null[base]")

    # --- overlays (pilulas / cards) ---------------------------------
    atual = "[base]"
    for i, o in enumerate(overlays):
        idx = base_n + i
        ent, sai = an["entrada_s"], an["saida_s"]
        t0, t1 = o["t0"], max(o["t1"], o["t0"] + ent + sai + 0.1)
        F.append(f"[{idx}:v]format=rgba,"
                 f"fade=t=in:st={t0:.3f}:d={ent}:alpha=1,"
                 f"fade=t=out:st={t1 - sai:.3f}:d={sai}:alpha=1[ov{i}]")
        dy = o.get("slide", an["slide_px"])
        y = (f"{o['y']}+{dy}*(1-min(1,max(0,(t-{t0:.3f})/{ent})))" if dy else str(o["y"]))
        prox = f"[st{i}]"
        F.append(f"{atual}[ov{i}]overlay={o['x']}:'{y}':"
                 f"enable='between(t,{t0:.3f},{t1:.3f})':format=auto{prox}")
        atual = prox

    # --- legendas ----------------------------------------------------
    if legendas_ass:
        cam = legendas_ass.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        F.append(f"{atual}subtitles='{cam}':alpha=1[vfim]")
    else:
        F.append(f"{atual}format=yuv420p[vfim]")

    # --- audio -------------------------------------------------------
    mus = tema["musica"]
    vol = trilha_volume if trilha_volume is not None else mus["volume_db"]
    if musica:
        entradas += ["-stream_loop", "-1", "-i", musica]
        im = base_n + len(overlays)
        F.append(f"[0:a]aformat=channel_layouts=stereo,aresample=48000,"
                 f"highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=8:release=180,"
                 f"asplit=2[voz][vsc]")
        F.append(f"[{im}:a]aformat=channel_layouts=stereo,aresample=48000,"
                 f"atrim=0:{dur:.3f},volume={vol}dB,"
                 f"afade=t=in:st=0:d={mus['fade_in_s']},"
                 f"afade=t=out:st={max(0, dur - mus['fade_out_s']):.3f}:d={mus['fade_out_s']}[mus]")
        F.append(f"[mus][vsc]sidechaincompress=threshold=0.055:ratio={mus['ducking_db']}:"
                 f"attack=12:release=320[musd]")
        F.append(f"[voz][musd]amix=inputs=2:duration=first:dropout_transition=0,"
                 f"loudnorm=I={s['audio_lufs']}:TP=-1.2:LRA=11[afim]")
    else:
        F.append(f"[0:a]aformat=channel_layouts=stereo,aresample=48000,highpass=f=70,"
                 f"loudnorm=I={s['audio_lufs']}:TP=-1.2:LRA=11[afim]")

    cmd = ["ffmpeg", "-v", "error", "-y", *entradas,
           "-filter_complex", ";".join(F),
           "-map", "[vfim]", "-map", "[afim]", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-profile:v", "high", "-level", "4.1",
           "-preset", s["preset"], "-crf", str(s["crf"]),
           "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-x264-params", "keyint=60:min-keyint=30:scenecut=0",
           "-c:a", "aac", "-b:a", s["audio_bitrate"], "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", saida]
    log(f"  renderizando {dur:.1f}s em {W}x{H}...")
    _exec(cmd, "na montagem final")
    return saida
