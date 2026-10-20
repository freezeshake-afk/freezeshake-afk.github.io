#!/usr/bin/env python3
"""Integra o pacote de cenas de martires a uma instalacao do editonny.

    python3 instalar.py              # instala ou atualiza as cenas
    python3 instalar.py --remover    # tira as cenas e restaura o catalogo
    python3 instalar.py --conferir   # so mostra o estado, nao muda nada

Rode de novo toda vez que atualizar o editonny: a atualizacao substitui a
pasta do pacote e leva junto as cenas de terceiros.
"""
import argparse
import json
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CENAS = os.path.join(AQUI, "scenes")
CATALOGO_PACOTE = os.path.join(AQUI, "catalog.martires.json")

CANDIDATOS = [
    os.path.expanduser("~/.local/share/editonny"),
    os.path.expanduser("~/.claude/skills/editonny"),
    os.path.expanduser("~/.agents/skills/editonny"),
]


def achar_editonny(indicado=None):
    for c in ([indicado] if indicado else []) + CANDIDATOS:
        if c and os.path.isfile(os.path.join(c, "SKILL.md")):
            return os.path.realpath(c)
    raise SystemExit(
        "[erro] editonny nao encontrado.\n"
        "       Instale primeiro (https://github.com/soumatheusgomes/editonny)\n"
        "       ou aponte a pasta: python3 instalar.py --editonny /caminho/para/editonny"
    )


def ler_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def escrever_json(caminho, dados):
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, caminho)


def ids_do_pacote():
    return [c["id"] for c in ler_json(CATALOGO_PACOTE)["scenes"]]


def estado(editonny):
    cat = ler_json(os.path.join(editonny, "visuals", "catalog.json"))
    presentes = {c["id"] for c in cat["scenes"]}
    meus = ids_do_pacote()
    instaladas = [i for i in meus if i in presentes]
    arquivos = [i for i in meus
                if os.path.isfile(os.path.join(editonny, "visuals", "scenes", i + ".html"))]
    return cat, instaladas, arquivos


def instalar(editonny):
    destino_cenas = os.path.join(editonny, "visuals", "scenes")
    catalogo = os.path.join(editonny, "visuals", "catalog.json")
    if not os.path.isdir(destino_cenas):
        raise SystemExit("[erro] pasta de cenas nao encontrada: %s" % destino_cenas)

    pacote = ler_json(CATALOGO_PACOTE)["scenes"]
    for entrada in pacote:
        origem = os.path.join(CENAS, entrada["id"] + ".html")
        if not os.path.isfile(origem):
            raise SystemExit("[erro] cena faltando: %s (rode construir.py)" % origem)

    # backup do catalogo antes do primeiro merge
    reserva = catalogo + ".antes-martires"
    cat = ler_json(catalogo)
    meus = {c["id"] for c in pacote}
    ja_tinha = {c["id"] for c in cat["scenes"]} & meus
    if not os.path.isfile(reserva) and not ja_tinha:
        shutil.copy2(catalogo, reserva)

    copiadas = 0
    for entrada in pacote:
        shutil.copy2(os.path.join(CENAS, entrada["id"] + ".html"),
                     os.path.join(destino_cenas, entrada["id"] + ".html"))
        copiadas += 1

    restantes = [c for c in cat["scenes"] if c["id"] not in meus]
    cat["scenes"] = restantes + pacote
    escrever_json(catalogo, cat)

    print("editonny: %s" % editonny)
    print("  %d cenas copiadas para visuals/scenes/" % copiadas)
    print("  catalogo: %d cenas no total (%d do pacote de martires)"
          % (len(cat["scenes"]), len(pacote)))
    if os.path.isfile(reserva):
        print("  catalogo original guardado em %s" % os.path.basename(reserva))
    print("\nConfira com:")
    print("  python3 %s/scripts/editonny.py catalog --search martir" % editonny)


def remover(editonny):
    catalogo = os.path.join(editonny, "visuals", "catalog.json")
    cat = ler_json(catalogo)
    meus = set(ids_do_pacote())
    antes = len(cat["scenes"])
    cat["scenes"] = [c for c in cat["scenes"] if c["id"] not in meus]
    escrever_json(catalogo, cat)
    apagadas = 0
    for i in meus:
        caminho = os.path.join(editonny, "visuals", "scenes", i + ".html")
        if os.path.isfile(caminho):
            os.remove(caminho)
            apagadas += 1
    print("removidas %d entradas do catalogo e %d arquivos de cena"
          % (antes - len(cat["scenes"]), apagadas))


def conferir(editonny):
    cat, instaladas, arquivos = estado(editonny)
    print("editonny: %s" % editonny)
    print("  catalogo com %d cenas" % len(cat["scenes"]))
    for i in ids_do_pacote():
        marca = "ok " if i in instaladas and i in arquivos else "NAO"
        print("  [%s] %s" % (marca, i))
    if len(instaladas) != len(ids_do_pacote()):
        print("\nFaltou alguma: rode 'python3 instalar.py'")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--editonny", help="pasta da instalacao do editonny")
    ap.add_argument("--remover", action="store_true")
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args()
    alvo = achar_editonny(a.editonny)
    if a.conferir:
        conferir(alvo)
    elif a.remover:
        remover(alvo)
    else:
        instalar(alvo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
