"""Le o roteiro (.txt com front-matter YAML + marcadores inline)."""
import re

import yaml

MARCADOR = re.compile(r"\[\[(.+?)\]\]", re.S)


class Marcador:
    def __init__(self, tipo, args, idx_palavra):
        self.tipo = tipo
        self.args = args
        self.idx = idx_palavra          # indice da palavra seguinte no roteiro
        self.t = None                   # preenchido no alinhamento

    def __repr__(self):
        return f"<{self.tipo} {self.args} @palavra{self.idx}>"


def _partes(corpo):
    return [p.strip() for p in corpo.split("|")]


def ler(caminho):
    bruto = open(caminho, encoding="utf-8").read()
    meta = {}
    if bruto.lstrip().startswith("---"):
        _, fm, bruto = bruto.lstrip().split("---", 2)
        meta = yaml.safe_load(fm) or {}

    palavras, marcadores, pos = [], [], 0
    for m in MARCADOR.finditer(bruto):
        palavras += bruto[pos:m.start()].split()
        pos = m.end()
        corpo = m.group(1).strip()
        if ":" in corpo:
            tipo, resto = corpo.split(":", 1)
            args = _partes(resto)
        else:
            tipo, args = corpo, []
        marcadores.append(Marcador(tipo.strip().lower().lstrip("/"), args, len(palavras)))
        if corpo.strip().startswith("/"):
            marcadores[-1].tipo = "fim_" + marcadores[-1].tipo
    palavras += bruto[pos:].split()
    return meta, palavras, marcadores
