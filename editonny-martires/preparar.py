#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere se o seu PC tem tudo para rodar o editonny + o pacote de martires,
e imprime o comando exato de instalacao do que faltar, no seu sistema.

    python3 preparar.py          (Windows:  py preparar.py)

So usa a biblioteca padrao, entao roda antes de voce instalar qualquer coisa.
Nao instala nada e nao muda nada: so olha e te diz o que fazer.
"""
from __future__ import print_function

import os
import platform
import shutil
import subprocess
import sys
import tempfile

SO = platform.system()                       # Windows / Darwin / Linux
WIN = SO == "Windows"
MAC = SO == "Darwin"
ARM_MAC = MAC and platform.machine() == "arm64"

ESPACO_GB = 5.0                              # pacote 1,1 GB + chromium 365 MB + modelo + folga

VERDE, VERM, AMAR, CINZA, FIM = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"
if WIN and not os.environ.get("WT_SESSION"):
    VERDE = VERM = AMAR = CINZA = FIM = ""   # console antigo do Windows nao pinta

achados = []                                 # (nivel, titulo, detalhe, comandos)


def cmd(mapa):
    """Comando do sistema atual; aviso generico se o SO for desconhecido."""
    return mapa.get(SO, "instale pelo site oficial do projeto")


def nota(nivel, titulo, detalhe="", comandos=None):
    achados.append((nivel, titulo, detalhe, comandos or []))
    marca = {"ok": VERDE + " ok " + FIM, "falta": VERM + "FALTA" + FIM,
             "aviso": AMAR + "aviso" + FIM}[nivel]
    linha = "  [%s] %s" % (marca, titulo)
    if detalhe:
        linha += CINZA + "  " + detalhe + FIM
    print(linha)


def saida(*args):
    try:
        r = subprocess.run(list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=25)
        return r.stdout.decode("utf-8", "replace").strip()
    except Exception:
        return ""


def versao_tupla(texto):
    numeros = []
    atual = ""
    for ch in texto:
        if ch.isdigit():
            atual += ch
        elif atual:
            numeros.append(int(atual))
            atual = ""
            if len(numeros) == 3:
                break
        elif numeros:
            break
    if atual:
        numeros.append(int(atual))
    while len(numeros) < 3:
        numeros.append(0)
    return tuple(numeros[:3])


# --------------------------------------------------------------- verificacoes

CMD_PYTHON = {"Windows": "winget install Python.Python.3.12",
              "Darwin": "brew install python@3.12",
              "Linux": "sudo apt install python3"}
CMD_UV = {"Windows": 'powershell -c "irm https://astral.sh/uv/install.ps1 | iex"',
          "Darwin": "brew install uv",
          "Linux": "curl -LsSf https://astral.sh/uv/install.sh | sh"}
CMD_NODE = {"Windows": "winget install OpenJS.NodeJS.LTS",
            "Darwin": "brew install node@22",
            "Linux": "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -"
                     " && sudo apt install -y nodejs"}
CMD_FFMPEG = {"Windows": "winget install Gyan.FFmpeg",
              "Darwin": "brew install ffmpeg",
              "Linux": "sudo apt install ffmpeg"}
CMD_TESS = {"Windows": "winget install UB-Mannheim.TesseractOCR",
            "Linux": "sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng"}
CMD_TESS_POR = {"Windows": "baixe por.traineddata de github.com/tesseract-ocr/tessdata"
                           " e ponha na pasta tessdata do Tesseract",
                "Linux": "sudo apt install tesseract-ocr-por"}


def ver_python():
    v = sys.version_info
    atual = "%d.%d.%d" % (v[0], v[1], v[2])
    if v[:2] >= (3, 9):
        nota("ok", "Python (lancador)", atual)
    else:
        nota("falta", "Python 3.9+ (lancador)", "achei " + atual, [cmd(CMD_PYTHON)])
    # o engine roda num ambiente separado; o uv baixa a versao certa se precisar
    if v[:2] >= (3, 14):
        nota("aviso", "Este Python e 3.14+",
             "o engine exige >=3.10 e <3.14; o uv baixa uma compativel sozinho")


def ver_uv():
    if shutil.which("uv"):
        nota("ok", "uv", saida("uv", "--version").split("\n")[0])
        return
    nota("falta", "uv", "monta o ambiente travado do engine", [cmd(CMD_UV)])


def ver_node():
    if not shutil.which("node"):
        nota("falta", "Node.js 22.13+ ou 24+", "renderiza as cenas (HyperFrames)",
             [cmd(CMD_NODE)])
        return
    bruto = saida("node", "-v")
    v = versao_tupla(bruto)
    if (v[0] == 22 and v[1] >= 13) or v[0] >= 24:
        nota("ok", "Node.js", bruto)
    else:
        nota("falta", "Node.js 22.13+ ou 24+", "achei " + bruto + ", nao serve",
             [cmd(CMD_NODE)])
    if not shutil.which("npx"):
        nota("falta", "npx", "vem junto com o Node; reinstale o Node", [cmd(CMD_NODE)])


def ver_ffmpeg():
    faltando = [n for n in ("ffmpeg", "ffprobe") if not shutil.which(n)]
    if not faltando:
        nota("ok", "FFmpeg e ffprobe", saida("ffmpeg", "-version").split("\n")[0][:46])
        return
    nota("falta", "FFmpeg/ffprobe", "faltando: " + ", ".join(faltando), [cmd(CMD_FFMPEG)])


def ver_ocr():
    """O editonny confere as legendas lendo os frames; sem leitor ele trava esse passo."""
    if MAC:
        if shutil.which("swiftc"):
            nota("ok", "OCR (Apple Vision)", "swiftc presente")
        else:
            nota("falta", "OCR (Apple Vision)", "precisa do compilador Swift",
                 ["xcode-select --install"])
        return
    exe = shutil.which("tesseract")
    if not exe:
        nota("falta", "OCR (Tesseract)", "confere as legendas no video final",
             [cmd(CMD_TESS)])
        return
    linguas = saida(exe, "--list-langs").lower().split()
    tem = [l for l in ("eng", "por", "spa") if l in linguas]
    if "por" in tem:
        nota("ok", "OCR (Tesseract)", "idiomas: " + ", ".join(tem))
    elif tem:
        nota("aviso", "OCR sem portugues",
             "achei: " + ", ".join(tem) + "; seus videos sao em pt", [cmd(CMD_TESS_POR)])
    else:
        nota("falta", "Idiomas do Tesseract", "nenhum de eng/por/spa instalado",
             [cmd(CMD_TESS)])


def ver_symlink():
    """O instalador do editonny cria links simbolicos; no Windows isso e restrito."""
    if not WIN:
        return
    base = tempfile.mkdtemp(prefix="editonny-link-")
    alvo = os.path.join(base, "alvo")
    os.makedirs(alvo)
    try:
        os.symlink(alvo, os.path.join(base, "link"), target_is_directory=True)
        nota("ok", "Links simbolicos", "o instalador vai conseguir registrar a skill")
    except OSError:
        nota("falta", "Links simbolicos bloqueados",
             "o instalador do editonny usa symlink e vai falhar", [
                 "Ligue o Modo Desenvolvedor:",
                 "  Configuracoes > Privacidade e seguranca > Para desenvolvedores",
                 "ou rode o install.py num terminal como Administrador"])
    finally:
        shutil.rmtree(base, ignore_errors=True)


def ver_espaco():
    try:
        livre = shutil.disk_usage(os.path.expanduser("~")).free / (1024.0 ** 3)
    except Exception:
        return
    texto = "%.1f GB livres" % livre
    if livre >= ESPACO_GB:
        nota("ok", "Espaco em disco", texto)
    else:
        nota("aviso", "Pouco espaco", texto + "; o conjunto pede ~%.0f GB" % ESPACO_GB,
             ["pacote 1,1 GB + navegador 365 MB + modelo de transcricao + seus videos"])


def ver_editonny():
    candidatos = [os.path.expanduser("~/.local/share/editonny"),
                  os.path.expanduser("~/.claude/skills/editonny"),
                  os.path.expanduser("~/.agents/skills/editonny")]
    achado = None
    for c in candidatos:
        if os.path.isfile(os.path.join(c, "SKILL.md")):
            achado = os.path.realpath(c)
            break
    if not achado:
        nota("falta", "editonny", "ainda nao instalado", [
            "git clone https://github.com/soumatheusgomes/editonny",
            "cd editonny",
            ("py install.py --target both" if WIN else "python3 install.py --target both")])
        return None
    try:
        with open(os.path.join(achado, "VERSION")) as f:
            v = f.read().strip()
    except OSError:
        v = "?"
    nota("ok", "editonny", "v" + v + "  " + achado)
    return achado


def ver_pacote(editonny):
    if not editonny:
        return
    cenas = ["martir-ficha", "martir-local", "martir-linha-tempo",
             "martir-escolha", "martir-contador", "martir-ultimas-palavras"]
    pasta = os.path.join(editonny, "visuals", "scenes")
    faltam = [c for c in cenas if not os.path.isfile(os.path.join(pasta, c + ".html"))]
    aqui = os.path.dirname(os.path.abspath(__file__))
    if not faltam:
        nota("ok", "Pacote de martires", "as 6 cenas estao instaladas")
    else:
        nota("falta", "Pacote de martires", "%d de 6 cenas faltando" % len(faltam), [
            "cd " + aqui,
            ("py instalar.py" if WIN else "python3 instalar.py")])


# --------------------------------------------------------------------- saida

def main():
    print("")
    print("  editonny + pacote de martires - o que falta no seu PC")
    print("  sistema: %s %s (%s)" % (SO, platform.release(), platform.machine()))
    if ARM_MAC:
        print(CINZA + "  Apple Silicon: a transcricao usa MLX Whisper" + FIM)
    else:
        print(CINZA + "  a transcricao usa Faster Whisper" + FIM)
    print("")

    ver_python()
    ver_uv()
    ver_node()
    ver_ffmpeg()
    ver_ocr()
    ver_symlink()
    ver_espaco()
    print("")
    editonny = ver_editonny()
    ver_pacote(editonny)
    print("")

    pendentes = [a for a in achados if a[0] == "falta"]
    avisos = [a for a in achados if a[0] == "aviso"]

    if not pendentes:
        print(VERDE + "  Tudo pronto." + FIM)
        if avisos:
            print("  Com %d aviso(s) acima - da pra rodar assim mesmo." % len(avisos))
        print("")
        print("  Confira o motor:")
        alvo = editonny or os.path.expanduser("~/.local/share/editonny")
        print("    %s %s doctor" % ("py" if WIN else "python3",
                                    os.path.join(alvo, "scripts", "editonny.py")))
        print("  Depois abra uma conversa nova no Claude Code e chame /editonny.")
        print("")
        return 0

    print(VERM + "  Falta instalar %d coisa(s), na ordem:" % len(pendentes) + FIM)
    print("")
    for n, (_, titulo, _, comandos) in enumerate(pendentes, 1):
        print("  %d) %s" % (n, titulo))
        for c in comandos:
            print("       " + c)
        print("")
    if avisos:
        print(AMAR + "  Avisos (nao impedem de rodar):" + FIM)
        for _, titulo, detalhe, comandos in avisos:
            print("     - %s%s" % (titulo, ": " + detalhe if detalhe else ""))
            for c in comandos:
                print("         " + c)
        print("")
    print("  Rode este script de novo depois para conferir.")
    print("")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
