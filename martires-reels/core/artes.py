"""Renderiza as artes (fundo, pilulas, cards, moldura e mascara do PiP) em PNG."""
import html as _html
import json
import os
import re
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(RAIZ, "templates")

CANDIDATOS_CHROME = [
    "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]


def achar_chrome():
    for c in CANDIDATOS_CHROME:
        if c and os.path.exists(c):
            return c
    raise RuntimeError(
        "Chromium nao encontrado. Instale com: npx playwright install chromium"
    )


def _preencher(tpl, vars):
    txt = open(os.path.join(TEMPLATES, tpl), encoding="utf-8").read()
    for k, v in vars.items():
        txt = txt.replace("{{%s}}" % k, str(v))
    return re.sub(r"\{\{[A-Z_]+\}\}", "", txt)


def render_html(tpl, vars, w, h, destino, recortar=False):
    """Renderiza um template para PNG. recortar=True corta as margens transparentes."""
    chrome = achar_chrome()
    with tempfile.TemporaryDirectory() as td:
        shutil.copy(os.path.join(TEMPLATES, "base.css"), td)
        pagina = os.path.join(td, "p.html")
        open(pagina, "w", encoding="utf-8").write(_preencher(tpl, vars))
        subprocess.run(
            [
                chrome, "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                "--force-color-profile=srgb", "--disable-lcd-text",
                "--default-background-color=00000000",
                "--virtual-time-budget=1500",
                f"--window-size={w},{h}",
                f"--screenshot={destino}", f"file://{pagina}",
            ],
            check=True, capture_output=True,
        )
    im = Image.open(destino).convert("RGBA")
    if recortar:
        caixa = im.split()[3].getbbox()
        if caixa:
            im = im.crop(caixa)
    im.save(destino)
    return im.size


# ---------------------------------------------------------------- artes

def fundo(tema, destino):
    s, f = tema["saida"], tema["fundo"]
    ga, gb = f["glow_topo"], f["glow_baixo"]
    render_html("fundo.html", {
        "W": s["w"], "H": s["h"], "COR_BASE": f["cor_base"],
        "GRID_COR": f["grid_cor"], "GRID_PX": f["grid_px"], "GRID_LINHA": f["grid_linha"],
        "GA_COR": ga["cor"], "GA_X": ga["x"], "GA_Y": ga["y"], "GA_RAIO": ga["raio"],
        "GB_COR": gb["cor"], "GB_X": gb["x"], "GB_Y": gb["y"], "GB_RAIO": gb["raio"],
    }, s["w"], s["h"], destino)
    return destino


def _geo_pip(tema):
    s, p = tema["saida"], tema["pip"]
    x, y = round(p["x"] * s["w"]), round(p["y"] * s["h"])
    w, h = round(p["w"] * s["w"]), round(p["h"] * s["h"])
    return x, y, w - w % 2, h - h % 2


def moldura_pip(tema, destino):
    s, p = tema["saida"], tema["pip"]
    x, y, w, h = _geo_pip(tema)
    b = p["borda_px"]
    render_html("moldura.html", {
        "W": s["w"], "H": s["h"], "X": x - b, "Y": y - b, "CW": w + 2 * b, "CH": h + 2 * b,
        "RAIO": p["raio"] + b, "BORDA": b, "BORDA_COR": p["borda_cor"], "GLOW": p["glow"],
    }, s["w"], s["h"], destino)
    return destino


def mascara_pip(tema, destino):
    """Mascara branca com cantos arredondados, do tamanho do PiP (para alphamerge)."""
    _, _, w, h = _geo_pip(tema)
    r = tema["pip"]["raio"]
    ss = 4  # supersampling para antialias
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255)
    m.resize((w, h), Image.LANCZOS).save(destino)
    return destino


def pilula(tema, destino, texto, icone=None, numero=None):
    p = tema["pilula"]
    esc = _html.escape(texto.upper())
    badge = ""
    pad_esq = p["padding_x"]
    if numero is not None:
        badge = f'<span class="b">{_html.escape(str(numero))}</span>'
        pad_esq = round(p["padding_x"] * 0.45)
    elif icone:
        badge = f'<span class="ico">{_html.escape(icone)}</span>'
    return render_html("pilula.html", {
        "ALTURA": p["altura"], "RAIO": p["raio"], "PAD": p["padding_x"], "PAD_ESQ": pad_esq,
        "FUNDO": p["fundo"], "BORDA": p["borda"], "GLOW": p["glow"],
        "FONTE": p["fonte_px"], "TEXTO": esc,
        "TEXTO_GRAD": p.get("texto_gradiente", p.get("texto_cor", "#fff")),
        "ICONE_COR": p.get("icone_cor", "#F06292"),
        "ICO_PX": round(p["fonte_px"] * 1.05),
        "BADGE_HTML": badge, "BADGE": round(p["altura"] * 0.62),
        "BADGE_PX": round(p["fonte_px"] * 0.88),
        "BADGE_FUNDO": p["badge_fundo"], "BADGE_TEXTO": p["badge_texto"],
    }, 1800, 400, destino, recortar=True)


def card(tema, destino, titulo, sub=None, icone=None, tag=None):
    s, c = tema["saida"], tema["card"]
    cw = round(c["w"] * s["w"])
    # <<texto>> vira gradiente
    tit = _html.escape(titulo)
    tit = re.sub(r"&lt;&lt;(.+?)&gt;&gt;", r"<em>\1</em>", tit).replace("\n", "<br>")
    return render_html("card.html", {
        "BODYW": cw + 160, "CW": cw, "RAIO": c["raio"], "FUNDO": c["fundo"],
        "BORDA": c["borda"], "GLOW": c["glow"], "PAD": round(cw * 0.085),
        "TITULO": tit, "TITULO_PX": c["titulo_px"], "TITULO_COR": c["titulo_cor"],
        "SUB_PX": c["sub_px"], "SUB_COR": c["sub_cor"], "DESTAQUE": c["destaque"],
        "ICO_PX": round(c["titulo_px"] * 1.25),
        "ICO_HTML": f'<span class="ico">{_html.escape(icone)}</span>' if icone else "",
        "SUB_HTML": f'<div class="s">{_html.escape(sub)}</div>' if sub else "",
        "TAG_HTML": f'<div class="tag">{_html.escape(tag.upper())}</div>' if tag else "",
    }, cw + 160, 1600, destino, recortar=True)


def carregar_tema(caminho=None):
    return json.load(open(caminho or os.path.join(RAIZ, "tema.json"), encoding="utf-8"))


def caixa_solida(png, limiar=250):
    """Retangulo visual (sem o brilho/sombra) dentro do PNG -> (x,y,w,h)."""
    im = Image.open(png).convert("RGBA")
    cx = im.split()[3].point(lambda v: 255 if v >= limiar else 0).getbbox()
    if not cx:
        return 0, 0, im.width, im.height
    return cx[0], cx[1], cx[2] - cx[0], cx[3] - cx[1]
