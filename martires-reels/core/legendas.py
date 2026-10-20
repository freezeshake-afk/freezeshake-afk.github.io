"""Gera legendas .ass no estilo da referencia: blocos de 2-3 palavras,
caixa alta, branco com contorno preto e um 'pop' na entrada."""
import re

CABECALHO = """[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: cheio,{FONTE},{TAM_C},{COR},{COR},{CONTORNO},&H90000000,-1,0,0,0,100,100,0.6,0,1,{OUT},{SOM},5,40,40,40,1
Style: board,{FONTE},{TAM_B},{COR},{COR},{CONTORNO},&H90000000,-1,0,0,0,100,100,0.6,0,1,{OUT},{SOM},5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

FIM_FRASE = re.compile(r"[.!?…:;]$")
PAUSA_VIRGULA = re.compile(r",$")


def _ass_cor(hexcor):
    h = hexcor.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _tc(s):
    s = max(0.0, s)
    h = int(s // 3600); m = int(s % 3600 // 60); seg = s % 60
    return f"{h}:{m:02d}:{seg:05.2f}"


def blocos(palavras, max_palavras=3, max_chars=24, pausa_corte=0.32):
    """Agrupa palavras em blocos curtos, cortando em pontuacao e pausas."""
    out, atual = [], []
    for i, p in enumerate(palavras):
        atual.append(p)
        texto = " ".join(x["w"] for x in atual)
        prox = palavras[i + 1] if i + 1 < len(palavras) else None
        pausa = (prox["s"] - p["e"]) if prox else 99
        quebra = (
            len(atual) >= max_palavras
            or len(texto) >= max_chars
            or FIM_FRASE.search(p["w"])
            or (PAUSA_VIRGULA.search(p["w"]) and len(atual) >= 2)
            or pausa >= pausa_corte
            or prox is None
        )
        if quebra:
            out.append({"s": atual[0]["s"], "e": atual[-1]["e"],
                        "texto": texto, "palavras": atual})
            atual = []
    return out


def gerar(caminho, palavras, tema, modos=None, max_palavras=None):
    """modos: lista [(t_inicio, 'cheio'|'board')] ordenada."""
    s, L = tema["saida"], tema["legenda"]
    modos = modos or [(0.0, "cheio")]

    def modo_em(t):
        atual = modos[0][1]
        for ti, m in modos:
            if ti <= t + 1e-6:
                atual = m
        return atual

    bs = blocos(palavras, max_palavras or L["palavras_por_bloco"],
            max_chars=L.get("max_chars", 18))
    linhas = []
    for i, b in enumerate(bs):
        texto = b["texto"].upper() if L["maiusculas"] else b["texto"]
        texto = re.sub(r"\s+", " ", texto).strip().replace("\\", "")
        texto = re.sub(r"[.,;:]+$", "", texto)   # a referencia nao mostra ponto/virgula
        modo = modo_em(b["s"])
        y = round((L["y_board"] if modo == "board" else L["y_cheio"]) * s["h"])
        fim = b["e"]
        if i + 1 < len(bs):
            fim = min(bs[i + 1]["s"], b["e"] + 0.45)
        fim = max(fim, b["s"] + 0.30)
        pop = r"\fscx92\fscy92\t(0,80,\fscx100\fscy100)" if L["pop"] else ""
        linhas.append(
            f"Dialogue: 0,{_tc(b['s'])},{_tc(fim)},{modo},,0,0,0,,"
            f"{{\\an5\\pos({s['w']//2},{y}){pop}}}{texto}"
        )

    cab = CABECALHO.format(
        W=s["w"], H=s["h"], FONTE=L["fonte"],
        TAM_C=L["tamanho_cheio"], TAM_B=L["tamanho_board"],
        COR=_ass_cor(L["cor"]), CONTORNO=_ass_cor(L["contorno_cor"]),
        OUT=L["contorno_px"], SOM=L["sombra_px"],
    )
    open(caminho, "w", encoding="utf-8").write(cab + "\n".join(linhas) + "\n")
    return caminho, bs
