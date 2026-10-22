#!/usr/bin/env python3
"""Renderiza as 6 cenas do pacote no motor real do editonny e guarda um frame
de cada uma, para conferir se animam e cabem na area do painel.

    python3 validar.py                 # projeto sintetico, lint + check + frames
    python3 validar.py --render        # tambem gera o mp4 inteiro
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from instalar import achar_editonny  # noqa: E402

# cena, inicio, fim  (um bloco de frame continuo cobre tudo)
ROTEIRO = [
    ("martir-ficha", 1.0, 7.0),
    ("martir-local", 7.5, 13.5),
    ("martir-linha-tempo", 14.0, 21.0),
    ("martir-escolha", 21.5, 28.0),
    ("martir-contador", 28.5, 33.5),
    ("martir-ultimas-palavras", 34.0, 40.5),
]
DURACAO = 42.0
CAIXA_MOLDURA = [36, 912, 1008, 990]


def rodar(*args, cwd=None):
    r = subprocess.run([str(a) for a in args], cwd=cwd, text=True,
                       capture_output=True, timeout=900)
    if r.returncode != 0:
        print(r.stdout[-3000:])
        print(r.stderr[-3000:], file=sys.stderr)
        raise SystemExit("[erro] falhou: %s" % " ".join(str(a) for a in args[:3]))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--editonny")
    ap.add_argument("--render", action="store_true", help="tambem renderiza o mp4")
    ap.add_argument("--saida", default=os.path.join(AQUI, "preview"))
    a = ap.parse_args()

    E = achar_editonny(a.editonny)
    engine = os.path.join(E, "engine")
    visuals = os.path.join(E, "visuals")
    trabalho = tempfile.mkdtemp(prefix="martires-validar-")
    print("editonny: %s\ntrabalho: %s\n" % (E, trabalho))

    # 1. corte sintetico (so para o motor ter um video e uma duracao)
    edit = os.path.join(trabalho, "edit")
    os.makedirs(os.path.join(edit, "transcripts"))
    rodar("ffmpeg", "-v", "error", "-f", "lavfi", "-i",
          "testsrc2=size=360x640:rate=24", "-f", "lavfi", "-i",
          "sine=frequency=330:sample_rate=48000", "-t", str(DURACAO),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
          os.path.join(edit, "cut.mp4"))
    with open(os.path.join(edit, "cut_timeline.json"), "w") as f:
        json.dump({"duration": DURACAO, "width": 360, "height": 640, "fps": 24,
                   "segments": [{"out_start": 0}]}, f)
    # transcricao sintetica cobrindo o video todo: sem legenda na tela, a
    # colisao entre o conteudo do painel e a faixa da legenda passa batida
    palavras, t = [], 0.3
    vocab = ["martir", "historia", "igreja", "fogueira", "coragem", "seculo", "palavra"]
    i = 0
    while t < DURACAO - 0.6:
        palavras.append({"text": vocab[i % len(vocab)], "start": round(t, 2),
                         "end": round(t + 0.38, 2)})
        t += 0.46; i += 1
    with open(os.path.join(edit, "transcripts", "cut.json"), "w") as f:
        json.dump({"words": palavras}, f)

    # 2. projeto
    projeto = os.path.join(trabalho, "projeto")
    rodar(sys.executable, os.path.join(engine, "project-template", "build.py"),
          "new", projeto, "--edit", edit)

    # 3. bloco de moldura continuo + desligar legendas (so queremos ver os paineis)
    pj = os.path.join(projeto, "project.json")
    cfg = json.load(open(pj, encoding="utf-8"))
    ini, fim = ROTEIRO[0][1], ROTEIRO[-1][2]
    cfg["frame"] = {"box": CAIXA_MOLDURA}
    cfg["blocks"] = [{"scene": "fullscreen", "start": 0, "end": ini, "zoom": 1.0},
                     {"scene": "frame", "start": ini, "end": fim},
                     {"scene": "fullscreen", "start": fim, "zoom": 1.0}]
    cfg["captions"] = {"enabled": True, "style": "standard", "maxWords": 3, "inFrame": True}
    cfg["style"] = "night"
    json.dump(cfg, open(pj, "w", encoding="utf-8"), indent=2)

    # 4. aplicar as cenas
    for cena, s, e in ROTEIRO:
        print("aplicando %-24s %5.1f -> %5.1f" % (cena, s, e))
        rodar(sys.executable, os.path.join(visuals, "apply.py"), "--project", projeto,
              "--use", cena, "--start", str(s), "--end", str(e))
    cfg = json.load(open(pj, encoding="utf-8"))
    if len(cfg.get("scenes", [])) != len(ROTEIRO):
        raise SystemExit("[erro] cenas registradas: %d de %d"
                         % (len(cfg.get("scenes", [])), len(ROTEIRO)))

    # 5. montar e conferir
    rodar(sys.executable, "build.py", "prepare", cwd=projeto)
    rodar(sys.executable, "build.py", "compose", cwd=projeto)
    for comando in (["lint"], ["check"]):
        print("HyperFrames: %s" % comando[0])
        rodar(sys.executable, "build.py", "hf", *comando, cwd=projeto)

    # 6. um frame no meio de cada cena
    instantes = [round(s + (e - s) * 0.62, 2) for _, s, e in ROTEIRO]
    print("HyperFrames: snapshot em %s" % instantes)
    rodar(sys.executable, "build.py", "hf", "snapshot", "--at",
          ",".join(str(t) for t in instantes), "--no-end", "--describe", "false",
          "--output", "snapshots", cwd=projeto)

    os.makedirs(a.saida, exist_ok=True)
    achados = sorted(f for f in os.listdir(os.path.join(projeto, "snapshots"))
                     if f.startswith("frame-") and f.endswith(".png"))
    for (cena, _, _), arquivo in zip(ROTEIRO, achados):
        shutil.copy2(os.path.join(projeto, "snapshots", arquivo),
                     os.path.join(a.saida, cena + ".png"))
    print("\n%d frames em %s" % (len(achados), a.saida))

    if a.render:
        print("HyperFrames: render")
        rodar(sys.executable, "build.py", "hf", "render", "--quality", "draft",
              "--fps", "24", "--output", "renders/martires.mp4", cwd=projeto)
        destino = os.path.join(a.saida, "martires-demo.mp4")
        shutil.copy2(os.path.join(projeto, "renders", "martires.mp4"), destino)
        print("video em %s" % destino)

    print("\nOK: as %d cenas passaram no lint e no check do motor." % len(ROTEIRO))


if __name__ == "__main__":
    main()
