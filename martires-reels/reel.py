#!/usr/bin/env python3
"""
reel.py - monta reels de Instagram no estilo da referencia, a partir
dos clipes gerados no Google Flow + um roteiro com marcadores.

    python3 reel.py roteiros/policarpo.txt
    python3 reel.py roteiros/policarpo.txt --sem-whisper --out out/policarpo.mp4
"""
import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import alinhar, artes, legendas, render, roteiro  # noqa: E402

RAIZ = os.path.dirname(os.path.abspath(__file__))
DUR_PADRAO = {"pilula": 4.2, "card": 5.4}


def log(*a):
    print(*a, flush=True)


def resolver_clipes(meta, pasta_roteiro, cli):
    if cli:
        alvos = cli
    elif meta.get("clipes"):
        alvos = meta["clipes"]
    else:
        alvos = [os.path.join(RAIZ, "clipes")]
    saida = []
    for a in alvos:
        cam = a if os.path.isabs(a) else os.path.join(pasta_roteiro, a)
        if not os.path.exists(cam):
            cam = os.path.join(RAIZ, a)
        if os.path.isdir(cam):
            achados = []
            for ext in ("mp4", "mov", "webm", "mkv", "MP4", "MOV"):
                achados += glob.glob(os.path.join(cam, f"*.{ext}"))
            saida += sorted(achados)
        elif os.path.exists(cam):
            saida.append(cam)
        else:
            raise SystemExit(f"[erro] clipe nao encontrado: {a}")
    if not saida:
        raise SystemExit("[erro] nenhum clipe .mp4 encontrado (coloque em clipes/)")
    return saida


def construir_overlays(marcadores, tema, dur, build):
    """Transforma os marcadores em PNGs posicionados no tempo."""
    s = tema["saida"]
    overlays, modos, abertos = [], [(0.0, "cheio")], {}
    n_pilula = 0

    def fechar(tipo, t):
        if tipo in abertos:
            abertos[tipo]["t1"] = max(t, abertos[tipo]["t0"] + 1.0)
            del abertos[tipo]

    for i, m in enumerate(marcadores):
        t = m.t
        if m.tipo in ("cheio", "board"):
            modos.append((t, m.tipo))
            continue
        if m.tipo.startswith("fim_"):
            fechar(m.tipo[4:], t)
            continue
        if m.tipo not in ("pilula", "card"):
            log(f"  [aviso] marcador desconhecido ignorado: {m.tipo}")
            continue

        fechar(m.tipo, t)
        png = os.path.join(build, f"_ov{i:02d}.png")
        if m.tipo == "pilula":
            icone, texto = (m.args + [""])[:2] if len(m.args) >= 2 else (None, m.args[0])
            if len(m.args) == 1:
                icone, texto = None, m.args[0]
            numero = None
            if icone and icone.strip().isdigit():
                numero, icone = icone.strip(), None
            elif icone == "":
                icone = None
            n_pilula += 1
            artes.pilula(tema, png, texto, icone=icone, numero=numero)
            bx, by, bw, bh = artes.caixa_solida(png)
            iw, ih = artes.Image.open(png).size
            x = round(s["w"] / 2 - (bx + bw / 2))
            y = round(tema["pilula"]["y"] * s["h"] - (by + bh / 2))
        else:
            a = m.args + [None] * 4
            icone, titulo, sub, tag = a[0] or None, a[1] or "", a[2] or None, a[3] or None
            if icone and len(icone) > 3 and not titulo:
                icone, titulo = None, icone
            artes.card(tema, png, titulo.replace("\\n", "\n"), sub=sub, icone=icone, tag=tag)
            bx, by, bw, bh = artes.caixa_solida(png)
            x = round(s["w"] / 2 - (bx + bw / 2))
            y = round(tema["card"]["y"] * s["h"] - by)

        item = {"png": png, "x": x, "y": y, "t0": t,
                "t1": min(dur, t + DUR_PADRAO[m.tipo])}
        overlays.append(item)
        abertos[m.tipo] = item

    for it in abertos.values():
        it["t1"] = min(dur, it["t1"])
    return overlays, modos


def modos_para_intervalos(modos, dur):
    ivs, ini = [], None
    for t, m in modos + [(dur, "cheio")]:
        if m == "board" and ini is None:
            ini = t
        elif m == "cheio" and ini is not None:
            ivs.append((ini, t))
            ini = None
    if ini is not None:
        ivs.append((ini, dur))
    return [(a, b) for a, b in ivs if b - a > 0.2]


def main():
    ap = argparse.ArgumentParser(description="Monta reels no estilo da referencia")
    ap.add_argument("roteiro")
    ap.add_argument("--clipes", nargs="*", help="arquivos ou pasta com os clipes do Flow")
    ap.add_argument("--musica", help="trilha de fundo (mp3/wav)")
    ap.add_argument("--out", help="arquivo de saida")
    ap.add_argument("--tema", default=os.path.join(RAIZ, "tema.json"))
    ap.add_argument("--sem-whisper", action="store_true",
                    help="alinha as legendas pela energia do audio (sem baixar modelo)")
    ap.add_argument("--modelo", default="small", help="modelo whisper (tiny/base/small/medium)")
    ap.add_argument("--zoom", action="store_true", help="zoom lento no modo cheio")
    ap.add_argument("--so-legendas", action="store_true", help="gera so o .ass e sai")
    args = ap.parse_args()

    tema = artes.carregar_tema(args.tema)
    pasta = os.path.dirname(os.path.abspath(args.roteiro))
    meta, palavras, marcadores = roteiro.ler(args.roteiro)
    log(f"roteiro: {len(palavras)} palavras, {len(marcadores)} marcadores")

    build = os.path.join(RAIZ, "build")
    os.makedirs(build, exist_ok=True)
    os.makedirs(os.path.join(RAIZ, "out"), exist_ok=True)

    clipes = resolver_clipes(meta, pasta, args.clipes)
    log(f"clipes: {len(clipes)}")
    for c in clipes:
        log(f"   - {os.path.basename(c)}")

    fala = os.path.join(build, "fala.mp4")
    log("juntando clipes...")
    render.juntar_clipes(clipes, tema, fala)
    dur = render.duracao(fala)
    log(f"   duracao total: {dur:.2f}s")

    wav = alinhar.extrair_wav(fala, os.path.join(build, "fala.wav"))
    log("alinhando roteiro com o audio...")
    palavras_t, modo_align = alinhar.alinhar(
        wav, palavras, usar_whisper=not args.sem_whisper,
        modelo=args.modelo, idioma=meta.get("idioma", "pt"))
    log(f"   alinhamento: {modo_align}")

    for m in marcadores:
        if m.idx < len(palavras_t):
            m.t = palavras_t[m.idx]["s"]
        elif palavras_t:
            m.t = palavras_t[-1]["e"]
        else:
            m.t = 0.0
        m.t = max(0.0, min(dur - 0.3, m.t))

    overlays, modos = construir_overlays(marcadores, tema, dur, build)
    ivs = modos_para_intervalos(modos, dur)
    log(f"   modo board: {len(ivs)} trecho(s)  |  overlays: {len(overlays)}")

    ass = os.path.join(build, "legendas.ass")
    _, blocos = legendas.gerar(ass, palavras_t, tema, modos)
    log(f"   legendas: {len(blocos)} blocos -> {ass}")
    if args.so_legendas:
        return

    musica = args.musica or meta.get("musica")
    if musica and not os.path.isabs(musica):
        for base in (pasta, RAIZ):
            if os.path.exists(os.path.join(base, musica)):
                musica = os.path.join(base, musica)
                break
    if musica and not os.path.exists(musica):
        log(f"  [aviso] trilha nao encontrada ({musica}); seguindo sem musica.")
        musica = None

    nome = meta.get("arquivo") or os.path.splitext(os.path.basename(args.roteiro))[0]
    saida = args.out or os.path.join(RAIZ, "out", f"{nome}.mp4")
    render.montar(fala, tema, saida, ivs, overlays, ass,
                  musica=musica, zoom_lento=args.zoom, log=log)
    log(f"\nPRONTO -> {saida}  ({render.duracao(saida):.1f}s)")


if __name__ == "__main__":
    main()
