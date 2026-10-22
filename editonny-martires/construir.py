#!/usr/bin/env python3
"""Gera as cenas HTML do pacote de martires no contrato do editonny.

Cada cena vira um arquivo em scenes/ e uma entrada em catalog.martires.json.
Rode este script depois de mexer no visual de qualquer cena.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "scenes")

# O painel ocupa a area de cima; o apresentador fica na moldura embaixo.
# Conteudo importante dentro de x 140..940 e y 230..850 (regra do editonny).
ESQUELETO = r"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><title>editonny - @@NOME@@</title></head>
<body>
<!-- @@NOME@@. @@QUANDO@@ -->

<template id="@@ID@@-template">
<style>
@font-face{font-family:"Inter";src:url("assets/visuals/fonts/inter-var-latin.woff2") format("woff2");font-weight:100 900;font-display:block}
@font-face{font-family:"Inter";src:url("assets/visuals/fonts/inter-var-latin-ext.woff2") format("woff2");font-weight:100 900;font-display:block;unicode-range:U+0100-02BA,U+1E00-1E9F,U+20A0-20C0}
@font-face{font-family:"Playfair";src:url("assets/visuals/fonts/Playfair.ttf") format("truetype");font-weight:400 900;font-display:block}
@font-face{font-family:"PlayfairIt";src:url("assets/visuals/fonts/Playfair-Italic.ttf") format("truetype");font-weight:400 900;font-display:block}
#root *{margin:0;padding:0;box-sizing:border-box}
#root{position:absolute;inset:0;overflow:hidden;font-family:"Inter",sans-serif;color:var(--tx);
  --bg:#0A0B0F; --tx:#ffffff; --ac:#F0A868; --ac2:#F2A3B8; --su:rgba(255,255,255,.70); --ln:rgba(255,255,255,.11);}

/* fundo medido do reel de referencia: base quase preta, grade de 90px e brilho quente no topo */
.mt-bg{position:absolute;left:0;top:0;width:1080px;height:992px;background:var(--bg);opacity:0;overflow:hidden}
.mt-bg i{position:absolute;left:0;top:0;width:1080px;height:992px;display:block;
  background-image:linear-gradient(to right,var(--ln) 1px,transparent 1px),linear-gradient(to bottom,var(--ln) 1px,transparent 1px);
  background-size:90px 90px}
.mt-bg u{position:absolute;left:0;top:0;width:1080px;height:992px;display:block;
  background:radial-gradient(ellipse 80% 46% at 50% 10%,rgba(255,135,55,.55) 0%,transparent 70%)}
.mt-bg s{position:absolute;left:0;top:0;width:1080px;height:992px;display:block;text-decoration:none;
  background:radial-gradient(ellipse 85% 70% at 50% 46%,transparent 38%,rgba(0,0,0,.6) 100%)}
.mt-layer{position:absolute;left:0;top:0;width:1080px;height:992px;opacity:0;overflow:hidden}

.mt-kicker{position:absolute;left:0;top:148px;width:1080px;text-align:center;font-size:26px;font-weight:800;
  letter-spacing:.34em;color:var(--ac);opacity:0;white-space:nowrap}
.mt-rule{position:absolute;left:470px;top:196px;width:140px;height:2px;background:var(--su);opacity:0}
.mt-note{position:absolute;left:0;width:1080px;text-align:center;opacity:0}
.mt-note span{display:inline-block;padding:16px 34px;border-radius:999px;background:var(--ac);color:#2B1020;
  font-size:30px;font-weight:800;letter-spacing:-.01em;white-space:nowrap}
@@CSS@@
</style>

<div id="root" data-composition-id="@@ID@@" data-width="1080" data-height="1920" data-duration="@@DUR@@">
<div class="mt-bg" id="@@ID@@-bg"><i></i><u></u><s></s></div>
<div class="mt-layer" id="@@ID@@-layer">
@@HTML@@
</div>
</div>

<script>
(function () {
  const C = (window.__scenes || {})["@@ID@@"] || { words: [], duration: @@DUR@@ };
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  var D = @@DUR@@, IR = { immediateRender: false };

  var P = {
@@PARAMS@@
  };

  function ext(x, y) { var o = {}, i; for (i in x) o[i] = x[i]; for (i in y) o[i] = y[i]; return o; }
  /* Scale tweens are converted to clipping or translation for the renderer contract. */
  function rec(axis, v) { v = Math.max(0, Math.min(1, v)); var p = (100 - v * 100).toFixed(2) + "%";
    return axis === "x" ? "inset(0% " + p + " 0% 0%)" : "inset(" + p + " 0% 0% 0%)"; }
  function lim(o, start) {
    var r = {}, i;
    for (i in o) {
      if (i === "scale" || i === "transformOrigin" || i === "svgOrigin") continue;
      if (i === "scaleX") { r.clipPath = rec("x", o[i]); continue; }
      if (i === "scaleY") { r.clipPath = rec("y", o[i]); continue; }
      r[i] = o[i];
    }
    if (start && ("scale" in o) && !("x" in r) && !("y" in r) && !("rotation" in r) && !("clipPath" in r)) r.y = 26;
    return r;
  }
  var T = {
    fromTo: function (s, x, y, t) { var X = lim(x, true), Y = lim(y, false); if (("y" in X) && !("y" in Y)) Y.y = 0; return tl.fromTo(s, X, Y, t); },
    to: function (s, y, t) { return tl.to(s, lim(y, false), t); },
    set: function (s, y, t) { return tl.set(s, lim(y, false), t); }
  };
  /* Format counters in a modifier so GSAP does not parse a grouped number as a decimal. */
  function countNumber(sel, start, end, t, dur, fmt, ease) {
    var f = fmt || function (v) { return String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, "."); };
    tl.fromTo(sel, { textContent: start }, { textContent: end, duration: dur, ease: ease || "power2.out",
      immediateRender: false, modifiers: { textContent: function (v) { return f(parseFloat(v)); } } }, t);
  }
  /* Recebe o elemento, nunca o id em string: o apply.py renomeia os IDs e so
     reescreve a busca quando o id aparece literal na chamada. Id solto nao casa. */
  function setTexto(e, v) { if (e) e.textContent = v; }
  function partes(v, sep) { return String(v == null ? "" : v).split(sep || "|").map(function (s) { return s.trim(); }).filter(Boolean); }

  function painel() {
    T.fromTo("#@@ID@@-bg", { opacity: 0 }, { opacity: 1, duration: .22 }, 0);
    T.to("#@@ID@@-bg", ext({ opacity: 0, duration: .22 }, IR), D - .22);
    T.fromTo("#@@ID@@-layer", { opacity: 0 }, { opacity: 1, duration: .22 }, 0);
    T.to("#@@ID@@-layer", ext({ opacity: 0, duration: .22 }, IR), D - .22);
  }
  function titulo(sel, t) { T.fromTo(sel, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .42, ease: "back.out(1.7)" }, t); }
  function sobe(sel, t, d) { T.fromTo(sel, { opacity: 0, y: d == null ? 60 : d }, { opacity: 1, y: 0, duration: .5, ease: "power3.out" }, t); }
  function selo(sel, t) { T.fromTo(sel, { opacity: 0, rotation: -22, y: -40 }, { opacity: 1, rotation: 0, y: 0, duration: .5, ease: "back.out(2.2)" }, t); }
  function aviso(sel, t) { T.fromTo(sel, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .36, ease: "back.out(2)" }, t); }
  function pulsa(sel, t) { T.to(sel, ext({ y: "-=10", duration: .14, yoyo: true, repeat: 1, ease: "power2.out" }, IR), t); }
  function revela(sel, t, dur) { T.fromTo(sel, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: dur || .5, ease: "power2.inOut" }, t); }

@@APLICAR@@

@@TIMELINE@@

  tl.to({}, { duration: D }, 0);
  window.__timelines["@@ID@@"] = tl;
})();
</script>
</template>
</body></html>
"""

CENAS = []


def cena(id, nome, quando, dur, params, css, html, aplicar, timeline,
         categoria="Martires", layout="frame", esconde_legendas=False, textos=None):
    CENAS.append(dict(id=id, nome=nome, quando=quando, dur=dur, params=params, css=css,
                      html=html, aplicar=aplicar, timeline=timeline, categoria=categoria,
                      layout=layout, esconde=esconde_legendas, textos=textos or []))


# --------------------------------------------------------------------------
# 1. Ficha do martir
# --------------------------------------------------------------------------
cena(
    id="martir-ficha", nome="Martyr record card", dur=6.0,
    quando="When introducing the martyr: name, years, city and a short note on a stone record card.",
    params='''    nome: "Policarpo de Esmirna", // Nome do martir, como e falado.
    anos: "c. 69 - 155 d.C.", // Periodo de vida ou o ano do martirio.
    cidade: "Esmirna, provincia da Asia", // Cidade e provincia romana.
    nota: "discipulo do apostolo Joao", // Linha curta de contexto; vazio esconde a pastilha.''',
    css=r"""
#f-card{position:absolute;left:190px;top:236px;width:700px;height:480px;border-radius:34px;
  background:linear-gradient(160deg,#1B1320 0%,#120C16 100%);border:1px solid rgba(255,190,150,.22);
  box-shadow:0 30px 80px rgba(0,0,0,.62);opacity:0}
#f-selo{position:absolute;left:470px;top:272px;width:140px;height:140px;border-radius:50%;
  background:linear-gradient(135deg,#F2A3B8,#F6C9A0);box-shadow:0 10px 36px rgba(240,150,90,.45);opacity:0}
#f-selo b{position:absolute;left:64px;top:30px;width:12px;height:80px;border-radius:3px;background:#2B1020}
#f-selo i{position:absolute;left:38px;top:56px;width:64px;height:12px;border-radius:3px;background:#2B1020}
#f-nome{position:absolute;left:220px;top:432px;width:640px;height:140px;display:flex;align-items:center;
  justify-content:center;text-align:center;font-family:"Playfair",serif;font-weight:800;font-size:76px;
  line-height:1.06;letter-spacing:-.015em;opacity:0}
#f-anos{position:absolute;left:220px;top:586px;width:640px;text-align:center;font-size:36px;font-weight:700;
  letter-spacing:.06em;color:var(--ac);opacity:0}
#f-linha{position:absolute;left:420px;top:640px;width:240px;height:1px;background:rgba(255,255,255,.22);opacity:0}
#f-cidade{position:absolute;left:220px;top:666px;width:640px;text-align:center;font-size:32px;font-weight:500;
  color:var(--su);opacity:0}
#f-nota{top:735px}""",
    html=r"""      <div class="mt-kicker" id="f-kicker">MARTIR</div>
      <div class="mt-rule" id="f-rule"></div>
      <div id="f-card"></div>
      <div id="f-selo"><b></b><i></i></div>
      <div id="f-nome">Policarpo de Esmirna</div>
      <div id="f-anos">c. 69 - 155 d.C.</div>
      <div id="f-linha"></div>
      <div id="f-cidade">Esmirna, provincia da Asia</div>
      <div class="mt-note" id="f-nota"><span id="f-nota-t">discipulo do apostolo Joao</span></div>""",
    aplicar=r"""  setTexto(document.getElementById("f-nome"), P.nome); setTexto(document.getElementById("f-anos"), P.anos); setTexto(document.getElementById("f-cidade"), P.cidade);
  /* O nome encolhe sozinho para nunca invadir a linha dos anos. */
  var elNome = document.getElementById("f-nome"), nq = String(P.nome || "").length;
  if (elNome) elNome.style.fontSize = (nq > 30 ? 48 : nq > 22 ? 58 : nq > 16 ? 66 : 76) + "px";
  if (P.nota) { setTexto(document.getElementById("f-nota-t"), P.nota); } else { var n = document.getElementById("f-nota"); if (n) n.style.display = "none"; }""",
    timeline=r"""  painel();
  titulo("#f-kicker", .12);
  T.fromTo("#f-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, .22);
  T.fromTo("#f-card", { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: .55, ease: "power3.out" }, .3);
  selo("#f-selo", .62);
  sobe("#f-nome", .86, 40);
  sobe("#f-anos", 1.06, 26);
  T.fromTo("#f-linha", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4 }, 1.2);
  sobe("#f-cidade", 1.3, 22);
  if (P.nota) aviso("#f-nota", 1.6);
  pulsa("#f-selo", 2.1);""",
    textos=["MARTIR", "Policarpo de Esmirna", "c. 69 - 155 d.C.",
            "Esmirna, provincia da Asia", "discipulo do apostolo Joao"],
)

# --------------------------------------------------------------------------
# 2. Linha do tempo das perseguicoes
# --------------------------------------------------------------------------
cena(
    id="martir-linha-tempo", nome="Persecution timeline", dur=7.0,
    quando="When placing the story among the Roman persecutions: a marker travels the timeline and stops on the chosen emperor.",
    params='''    marcos: "Nero 64|Domiciano 95|Trajano 112|Antonino 155|Decio 250", // Ate 6 marcos "Nome Ano", separados por |.
    destaque: 4, // Qual marco acende, contando de 1.
    titulo: "Perseguicoes no Imperio", // Titulo do painel.
    nota: "o ano em que Policarpo morreu", // Pastilha que aparece no fim; vazio esconde.''',
    css=r"""
#t-titulo{position:absolute;left:0;top:206px;width:1080px;text-align:center;font-family:"Playfair",serif;
  font-weight:700;font-size:58px;letter-spacing:-.01em;opacity:0}
#t-eixo{position:absolute;left:140px;top:560px;width:800px;height:4px;border-radius:2px;background:rgba(255,255,255,.18)}
#t-preenche{position:absolute;left:0;top:0;width:800px;height:4px;border-radius:2px;
  background:linear-gradient(90deg,#F2A3B8,#F0A868)}
.t-marco{position:absolute;top:546px;width:200px;margin-left:-100px;text-align:center;opacity:0}
.t-marco em{position:absolute;left:98px;top:0;width:4px;height:28px;border-radius:2px;background:rgba(255,255,255,.4);font-style:normal}
.t-marco b{position:absolute;left:0;top:44px;width:200px;font-size:34px;font-weight:800;letter-spacing:-.01em;
  font-variant-numeric:tabular-nums}
.t-marco span{position:absolute;left:15px;top:-54px;width:170px;font-size:23px;font-weight:700;letter-spacing:.08em;
  color:var(--su)}
.t-marco.on em{background:var(--ac);height:40px;top:-6px}
.t-marco.on b{color:var(--ac);font-size:44px;top:46px}
.t-marco.on span{color:var(--tx)}
#t-bola{position:absolute;top:548px;left:140px;width:30px;height:30px;margin:-13px 0 0 -15px;border-radius:50%;
  background:#fff;box-shadow:0 0 0 10px rgba(240,168,104,.3),0 0 34px var(--ac);opacity:0}
#t-nota{top:700px}""",
    html=r"""      <div class="mt-kicker" id="t-kicker">LINHA DO TEMPO</div>
      <div class="mt-rule" id="t-rule"></div>
      <div id="t-titulo">Perseguicoes no Imperio</div>
      <div id="t-eixo"><div id="t-preenche"></div></div>
      <div id="t-marcos">
        <div class="t-marco" id="t-m0"><span></span><em></em><b></b></div>
        <div class="t-marco" id="t-m1"><span></span><em></em><b></b></div>
        <div class="t-marco" id="t-m2"><span></span><em></em><b></b></div>
        <div class="t-marco" id="t-m3"><span></span><em></em><b></b></div>
        <div class="t-marco" id="t-m4"><span></span><em></em><b></b></div>
        <div class="t-marco" id="t-m5"><span></span><em></em><b></b></div>
      </div>
      <div id="t-bola"></div>
      <div class="mt-note" id="t-nota"><span id="t-nota-t">o ano em que Policarpo morreu</span></div>""",
    aplicar=r"""  setTexto(document.getElementById("t-titulo"), P.titulo);
  /* Marcos sao estaticos: o apply.py renomeia IDs literais, mas nao classes
     montadas no JS, entao nada aqui pode criar elemento ou concatenar classe. */
  var M = partes(P.marcos).slice(0, 6); if (!M.length) M = ["Marco 1"];
  var alvo = Math.min(Math.max(1, P.destaque | 0), M.length);
  var passo = M.length > 1 ? 800 / (M.length - 1) : 0;
  var larg = Math.max(90, Math.min(190, (passo || 200) - 14));
  var marcos = [document.getElementById("t-m0"), document.getElementById("t-m1"),
                document.getElementById("t-m2"), document.getElementById("t-m3"),
                document.getElementById("t-m4"), document.getElementById("t-m5")];
  for (var i = 0; i < marcos.length; i++) {
    var el = marcos[i]; if (!el) continue;
    if (i >= M.length) { el.style.display = "none"; continue; }
    var corte = M[i].lastIndexOf(" "), sp = el.children[0], tick = el.children[1], bb = el.children[2];
    el.style.left = (140 + passo * i) + "px";
    sp.textContent = corte > 0 ? M[i].slice(0, corte) : M[i];
    bb.textContent = corte > 0 ? M[i].slice(corte + 1) : "";
    sp.style.width = larg + "px"; sp.style.left = ((200 - larg) / 2) + "px";
    if (i + 1 === alvo) {
      tick.style.background = "var(--ac)"; tick.style.height = "40px"; tick.style.top = "-6px";
      bb.style.color = "var(--ac)"; bb.style.fontSize = "44px"; bb.style.top = "46px";
      sp.style.color = "var(--tx)";
    }
  }
  if (P.nota) { setTexto(document.getElementById("t-nota-t"), P.nota); } else { var tn = document.getElementById("t-nota"); if (tn) tn.style.display = "none"; }
  var fim = 140 + passo * (alvo - 1), frac = (fim - 140) / 800;""",
    timeline=r"""  painel();
  titulo("#t-kicker", .12);
  T.fromTo("#t-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, .2);
  sobe("#t-titulo", .3, 40);
  T.fromTo("#t-preenche", { scaleX: 0 }, { scaleX: frac, duration: 1.5, ease: "power2.inOut" }, .9);
  var ent = { opacity: 0, y: 24 }, sai = { opacity: 1, y: 0, duration: .34, ease: "power3.out" };
  T.fromTo("#t-m0", ent, sai, .70); T.fromTo("#t-m1", ent, sai, .84);
  T.fromTo("#t-m2", ent, sai, .98); T.fromTo("#t-m3", ent, sai, 1.12);
  T.fromTo("#t-m4", ent, sai, 1.26); T.fromTo("#t-m5", ent, sai, 1.40);
  T.fromTo("#t-bola", { opacity: 0, x: 0 }, { opacity: 1, x: 0, duration: .25 }, .85);
  T.to("#t-bola", ext({ x: fim - 140, duration: 1.5, ease: "power2.inOut" }, IR), .9);
  if (alvo === 1) pulsa("#t-m0", 2.5); else if (alvo === 2) pulsa("#t-m1", 2.5);
  else if (alvo === 3) pulsa("#t-m2", 2.5); else if (alvo === 4) pulsa("#t-m3", 2.5);
  else if (alvo === 5) pulsa("#t-m4", 2.5); else pulsa("#t-m5", 2.5);
  if (P.nota) aviso("#t-nota", 2.8);""",
    textos=["LINHA DO TEMPO", "Perseguicoes no Imperio", "Nero 64", "Decio 250",
            "o ano em que Policarpo morreu"],
)

# --------------------------------------------------------------------------
# 3. Ultimas palavras
# --------------------------------------------------------------------------
cena(
    id="martir-ultimas-palavras", nome="Last words quote", dur=6.5,
    esconde_legendas=True,   # o painel ja mostra a fala; legenda junto seria texto dobrado
    quando="For the emotional peak: the martyr's recorded words appear line by line with the attribution below.",
    params='''    citacao: "Oitenta e seis anos eu o sirvo|e ele nunca me fez mal algum.|Como posso blasfemar do meu Rei,|que me salvou?", // Linhas da citacao, separadas por |.
    autor: "Policarpo de Esmirna, 155 d.C.", // Quem disse e quando.
    fonte: "Martirio de Policarpo, 9.3", // Referencia da fonte; vazio esconde.''',
    css=r"""
#q-aspas{position:absolute;left:0;top:188px;width:1080px;text-align:center;font-family:"Playfair",serif;
  font-weight:900;font-size:200px;line-height:1;color:var(--ac);opacity:0}
#q-linhas{position:absolute;left:120px;top:356px;width:840px;text-align:center}
.q-l{font-family:"PlayfairIt",serif;font-weight:500;font-size:58px;line-height:1.3;opacity:0;white-space:nowrap}
#q-barra{position:absolute;left:490px;top:0;width:100px;height:2px;background:var(--ac);opacity:0}
#q-autor{position:absolute;left:120px;width:840px;text-align:center;font-size:34px;font-weight:700;
  letter-spacing:.04em;color:var(--ac);opacity:0}
#q-fonte{position:absolute;left:120px;width:840px;text-align:center;font-size:26px;font-weight:500;
  letter-spacing:.08em;color:var(--su);opacity:0}""",
    html=r"""      <div id="q-aspas">&ldquo;</div>
      <div id="q-linhas">
        <div class="q-l" id="q-l0"></div>
        <div class="q-l" id="q-l1"></div>
        <div class="q-l" id="q-l2"></div>
        <div class="q-l" id="q-l3"></div>
        <div class="q-l" id="q-l4"></div>
      </div>
      <div id="q-barra"></div>
      <div id="q-autor">Policarpo de Esmirna, 155 d.C.</div>
      <div id="q-fonte">Martirio de Policarpo, 9.3</div>""",
    aplicar=r"""  var L = partes(P.citacao).slice(0, 5); if (!L.length) L = [" "];
  var linhas = [document.getElementById("q-l0"), document.getElementById("q-l1"),
                document.getElementById("q-l2"), document.getElementById("q-l3"),
                document.getElementById("q-l4")];
  for (var i = 0; i < linhas.length; i++) {
    if (!linhas[i]) continue;
    if (i < L.length) { linhas[i].textContent = L[i]; } else { linhas[i].style.display = "none"; }
  }
  var baseY = 356 + L.length * 58 * 1.3 + 44;
  var ba = document.getElementById("q-barra"); if (ba) ba.style.top = baseY + "px";
  var au = document.getElementById("q-autor"); if (au) { au.textContent = P.autor; au.style.top = (baseY + 34) + "px"; }
  var fo = document.getElementById("q-fonte");
  if (P.fonte && fo) { fo.textContent = P.fonte; fo.style.top = (baseY + 92) + "px"; }
  else if (fo) { fo.style.display = "none"; }""",
    timeline=r"""  painel();
  T.fromTo("#q-aspas", { opacity: 0, y: -40 }, { opacity: .5, y: 0, duration: .5, ease: "power3.out" }, .15);
  var eq = { opacity: 0, y: 34 }, sq = { opacity: 1, y: 0, duration: .46, ease: "power3.out" };
  T.fromTo("#q-l0", eq, sq, .55); T.fromTo("#q-l1", eq, sq, .85);
  T.fromTo("#q-l2", eq, sq, 1.15); T.fromTo("#q-l3", eq, sq, 1.45);
  T.fromTo("#q-l4", eq, sq, 1.75);
  var fimLinhas = .55 + L.length * .3;
  T.fromTo("#q-barra", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, fimLinhas + .1);
  sobe("#q-autor", fimLinhas + .25, 22);
  if (P.fonte) sobe("#q-fonte", fimLinhas + .45, 16);""",
    textos=["Oitenta e seis anos eu o sirvo", "Como posso blasfemar do meu Rei, que me salvou?",
            "Policarpo de Esmirna, 155 d.C.", "Martirio de Policarpo, 9.3"],
)

# --------------------------------------------------------------------------
# 4. Contador
# --------------------------------------------------------------------------
cena(
    id="martir-contador", nome="Martyr number counter", dur=5.0,
    quando="When a single number carries the weight: years of service, age, how many died, how long the persecution lasted.",
    params='''    valor: 86, // Numero final.
    de: 0, // Numero inicial da contagem.
    unidade: "anos", // Sufixo pequeno ao lado do numero; vazio esconde.
    rotulo: "SERVINDO A CRISTO", // Linha curta acima do numero.
    nota: "e ele nao negaria na ultima hora", // Pastilha abaixo; vazio esconde.''',
    css=r"""
#c-rotulo{position:absolute;left:0;top:330px;width:1080px;text-align:center;font-size:32px;font-weight:800;
  letter-spacing:.24em;color:var(--ac);opacity:0}
#c-num{position:absolute;left:0;top:372px;width:1080px;text-align:center;font-weight:800;font-size:250px;
  line-height:1;letter-spacing:-.05em;font-variant-numeric:tabular-nums;opacity:0;white-space:nowrap}
#c-num small{font-size:72px;font-weight:600;letter-spacing:-.02em;margin-left:16px;color:var(--su)}
#c-linha{position:absolute;left:420px;top:672px;width:240px;height:2px;background:rgba(255,255,255,.2);opacity:0}
#c-nota{top:718px}""",
    html=r"""      <div class="mt-kicker" id="c-kicker">O NUMERO</div>
      <div class="mt-rule" id="c-rule"></div>
      <div id="c-rotulo">SERVINDO A CRISTO</div>
      <div id="c-num"><span id="c-v">0</span><small id="c-u">anos</small></div>
      <div id="c-linha"></div>
      <div class="mt-note" id="c-nota"><span id="c-nota-t">e ele nao negaria na ultima hora</span></div>""",
    aplicar=r"""  setTexto(document.getElementById("c-rotulo"), P.rotulo);
  var un = document.getElementById("c-u");
  if (P.unidade) { un.textContent = P.unidade; } else { un.style.display = "none"; }
  if (P.nota) { setTexto(document.getElementById("c-nota-t"), P.nota); } else { var cn = document.getElementById("c-nota"); if (cn) cn.style.display = "none"; }
  var vi = Number(P.de) || 0, vf = Number(P.valor) || 0;""",
    timeline=r"""  painel();
  titulo("#c-kicker", .12);
  T.fromTo("#c-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, .2);
  sobe("#c-rotulo", .34, 28);
  T.fromTo("#c-num", { opacity: 0, y: 54 }, { opacity: 1, y: 0, duration: .48, ease: "expo.out" }, .54);
  countNumber("#c-v", vi, vf, .62, 1.5, function (v) { return String(Math.round(v)); }, "power2.out");
  pulsa("#c-num", 2.18);
  T.fromTo("#c-linha", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4 }, 2.3);
  if (P.nota) aviso("#c-nota", 2.45);""",
    textos=["O NUMERO", "SERVINDO A CRISTO", "86", "anos", "e ele nao negaria na ultima hora"],
)

# --------------------------------------------------------------------------
# 5. A escolha
# --------------------------------------------------------------------------
cena(
    id="martir-escolha", nome="The choice", dur=6.5,
    quando="When the martyr is offered a way out: two options appear, one is crossed out and the other lights up.",
    params='''    titulo: "A ESCOLHA", // Linha curta no topo.
    opcaoA: "Jurar pelo imperador", // Texto da opcao da esquerda.
    detalheA: "e sair vivo do estadio", // Linha menor da opcao A; vazio esconde.
    opcaoB: "Nao negar o Cristo", // Texto da opcao da direita.
    detalheB: "e morrer na fogueira", // Linha menor da opcao B; vazio esconde.
    escolhida: "B", // Qual acende: "A" ou "B". A outra e riscada.''',
    css=r"""
.e-card{position:absolute;top:290px;width:356px;height:400px;border-radius:30px;
  background:linear-gradient(160deg,#17121E 0%,#110C15 100%);border:1px solid rgba(255,255,255,.12);
  box-shadow:0 24px 60px rgba(0,0,0,.55);opacity:0}
#e-a{left:142px} #e-b{left:582px}
.e-card b{position:absolute;left:36px;top:150px;width:284px;font-size:40px;font-weight:800;line-height:1.16;
  letter-spacing:-.015em}
.e-card span{position:absolute;left:36px;top:280px;width:284px;font-size:28px;font-weight:500;line-height:1.3;color:var(--su)}
.e-card i{position:absolute;left:36px;top:46px;width:62px;height:62px;border-radius:50%;
  background:rgba(255,255,255,.1);font-style:normal;font-size:30px;font-weight:800;line-height:62px;text-align:center}
.e-risco{position:absolute;top:468px;left:150px;width:340px;height:11px;border-radius:6px;background:#E2503F;
  box-shadow:0 0 18px rgba(226,80,63,.6);
  opacity:0;clip-path:inset(0% 100% 0% 0%)}
#e-brilho{position:absolute;left:574px;top:282px;width:372px;height:416px;border-radius:34px;
  border:3px solid var(--ac);box-shadow:0 0 46px rgba(240,168,104,.55);opacity:0}
#e-nota{top:720px}""",
    html=r"""      <div class="mt-kicker" id="e-kicker">A ESCOLHA</div>
      <div class="mt-rule" id="e-rule"></div>
      <div class="e-card" id="e-a"><i>A</i><b id="e-at" data-layout-allow-occlusion>Jurar pelo imperador</b><span id="e-ad">e sair vivo do estadio</span></div>
      <div class="e-card" id="e-b"><i>B</i><b id="e-bt" data-layout-allow-occlusion>Nao negar o Cristo</b><span id="e-bd">e morrer na fogueira</span></div>
      <div class="e-risco" id="e-risco"></div>
      <div id="e-brilho"></div>
      <div class="mt-note" id="e-nota"><span id="e-nota-t">ele escolheu a segunda</span></div>""",
    aplicar=r"""  setTexto(document.getElementById("e-kicker"), P.titulo); setTexto(document.getElementById("e-at"), P.opcaoA); setTexto(document.getElementById("e-bt"), P.opcaoB);
  var ad = document.getElementById("e-ad"), bd = document.getElementById("e-bd");
  if (P.detalheA) { ad.textContent = P.detalheA; } else { ad.style.display = "none"; }
  if (P.detalheB) { bd.textContent = P.detalheB; } else { bd.style.display = "none"; }
  var escB = String(P.escolhida || "B").toUpperCase() !== "A";
  var risco = document.getElementById("e-risco"), brilho = document.getElementById("e-brilho");
  risco.style.left = (escB ? 150 : 590) + "px";
  brilho.style.left = (escB ? 574 : 134) + "px";
  var apagada = escB ? "#e-a" : "#e-b";
  var en = document.getElementById("e-nota"); if (en) en.style.display = "none";""",
    timeline=r"""  painel();
  titulo("#e-kicker", .12);
  T.fromTo("#e-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, .2);
  T.fromTo("#e-a", { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: .5, ease: "power3.out" }, .4);
  T.fromTo("#e-b", { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: .5, ease: "power3.out" }, .58);
  T.fromTo("#e-risco", { opacity: 1, clipPath: "inset(0% 100% 0% 0%)" }, { opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: .4, ease: "power2.inOut" }, 2.1);
  T.to(apagada, ext({ opacity: .46, duration: .4, ease: "power2.out" }, IR), 2.2);
  T.fromTo("#e-brilho", { opacity: 0 }, { opacity: 1, duration: .4, ease: "power2.out" }, 2.5);
  T.to("#e-brilho", ext({ opacity: .55, duration: .9, yoyo: true, repeat: 2, ease: "sine.inOut" }, IR), 3.0);""",
    textos=["A ESCOLHA", "Jurar pelo imperador", "Nao negar o Cristo",
            "e sair vivo do estadio", "e morrer na fogueira"],
)

# --------------------------------------------------------------------------
# 6. Onde aconteceu
# --------------------------------------------------------------------------
cena(
    id="martir-local", nome="Where it happened", dur=6.0,
    quando="When naming the place: a locator pulses over a map grid with the city, the Roman province and the year.",
    params='''    cidade: "ESMIRNA", // Nome da cidade, como e falada.
    provincia: "provincia romana da Asia", // Provincia ou regiao.
    ano: "155 d.C.", // Ano ou periodo; vazio esconde.
    nota: "hoje Izmir, na Turquia", // Pastilha abaixo; vazio esconde.''',
    css=r"""
#l-campo{position:absolute;left:140px;top:220px;width:800px;height:360px;border-radius:28px;overflow:hidden;
  background:radial-gradient(ellipse 70% 70% at 50% 50%,rgba(240,168,104,.14) 0%,transparent 72%),#0D0E14;
  border:1px solid rgba(255,255,255,.1);opacity:0}
#l-campo i{position:absolute;left:0;top:0;width:800px;height:360px;display:block;
  background-image:linear-gradient(to right,rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.07) 1px,transparent 1px);
  background-size:50px 50px}
.l-pt{position:absolute;width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.22)}
.l-anel{position:absolute;left:540px;top:400px;width:0;height:0;border-radius:50%;
  box-shadow:0 0 0 3px var(--ac);opacity:0}
#l-ponto{position:absolute;left:526px;top:386px;width:28px;height:28px;border-radius:50%;background:var(--ac);
  box-shadow:0 0 30px var(--ac);opacity:0}
#l-haste{position:absolute;left:538px;top:290px;width:4px;height:110px;background:linear-gradient(to bottom,transparent,var(--ac));opacity:0}
#l-cidade{position:absolute;left:0;top:606px;width:1080px;text-align:center;font-family:"Playfair",serif;
  font-weight:800;font-size:76px;letter-spacing:.03em;opacity:0}
#l-prov{position:absolute;left:0;top:700px;width:1080px;text-align:center;font-size:32px;font-weight:500;
  color:var(--su);opacity:0}
#l-ano{position:absolute;left:0;top:252px;width:1080px;text-align:center;font-size:30px;font-weight:800;
  letter-spacing:.2em;color:var(--ac);opacity:0}
#l-nota{top:752px}""",
    html=r"""      <div class="mt-kicker" id="l-kicker">ONDE ACONTECEU</div>
      <div class="mt-rule" id="l-rule"></div>
      <div id="l-campo"><i></i>
        <b class="l-pt" style="left:118px;top:78px"></b><b class="l-pt" style="left:252px;top:260px"></b>
        <b class="l-pt" style="left:596px;top:108px"></b><b class="l-pt" style="left:680px;top:288px"></b>
        <b class="l-pt" style="left:430px;top:54px"></b><b class="l-pt" style="left:158px;top:195px"></b>
      </div>
      <div id="l-ano">155 d.C.</div>
      <div class="l-anel" id="l-r1"></div>
      <div class="l-anel" id="l-r2"></div>
      <div class="l-anel" id="l-r3"></div>
      <div id="l-haste"></div>
      <div id="l-ponto"></div>
      <div id="l-cidade">ESMIRNA</div>
      <div id="l-prov">provincia romana da Asia</div>
      <div class="mt-note" id="l-nota"><span id="l-nota-t">hoje Izmir, na Turquia</span></div>""",
    aplicar=r"""  setTexto(document.getElementById("l-cidade"), P.cidade); setTexto(document.getElementById("l-prov"), P.provincia);
  var an = document.getElementById("l-ano");
  if (P.ano) { an.textContent = P.ano; } else { an.style.display = "none"; }
  if (P.nota) { setTexto(document.getElementById("l-nota-t"), P.nota); } else { var ln = document.getElementById("l-nota"); if (ln) ln.style.display = "none"; }""",
    timeline=r"""  painel();
  titulo("#l-kicker", .12);
  T.fromTo("#l-rule", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: .4, ease: "power2.out" }, .2);
  T.fromTo("#l-campo", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .5, ease: "power3.out" }, .3);
  if (P.ano) sobe("#l-ano", .55, 20);
  T.fromTo("#l-haste", { opacity: 0, y: -70 }, { opacity: 1, y: 0, duration: .4, ease: "power3.in" }, .8);
  T.fromTo("#l-ponto", { opacity: 0 }, { opacity: 1, duration: .2 }, 1.12);
  for (var j = 0; j < 3; j++) {
    T.fromTo("#l-r" + (j + 1), { opacity: .9, width: 0, height: 0, x: 0, y: 0 },
      { opacity: 0, width: 300, height: 300, x: -150, y: -150, duration: 1.6, ease: "power2.out" }, 1.2 + j * .45);
  }
  sobe("#l-cidade", 1.5, 36);
  sobe("#l-prov", 1.7, 22);
  if (P.nota) aviso("#l-nota", 1.95);""",
    textos=["ONDE ACONTECEU", "ESMIRNA", "provincia romana da Asia", "155 d.C.", "hoje Izmir, na Turquia"],
)


# --------------------------------------------------------------------------

def construir():
    os.makedirs(SAIDA, exist_ok=True)
    entradas = []
    for c in CENAS:
        html = (ESQUELETO
                .replace("@@ID@@", c["id"])
                .replace("@@NOME@@", c["nome"])
                .replace("@@QUANDO@@", c["quando"])
                .replace("@@DUR@@", "%g" % c["dur"])
                .replace("@@CSS@@", c["css"].strip("\n"))
                .replace("@@HTML@@", c["html"])
                .replace("@@PARAMS@@", c["params"])
                .replace("@@APLICAR@@", c["aplicar"])
                .replace("@@TIMELINE@@", c["timeline"]))
        caminho = os.path.join(SAIDA, c["id"] + ".html")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(html)

        par = {}
        for linha in c["params"].splitlines():
            linha = linha.strip()
            if not linha or "//" not in linha or ":" not in linha:
                continue
            chave, resto = linha.split(":", 1)
            valor, resumo = resto.rsplit("//", 1)
            valor = valor.strip().rstrip(",").strip()
            try:
                valor = json.loads(valor)
            except ValueError:
                pass
            par[chave.strip()] = {"default": valor, "summary": resumo.strip()}

        entradas.append({
            "id": c["id"],
            "file": "compositions/scenes/visuals/%s.html" % c["id"],
            "name": c["nome"],
            "category": c["categoria"],
            "whenToUse": c["quando"],
            "duration": c["dur"],
            "format": "9:16",
            "layout": c["layout"],
            "parameters": par,
            "hidesCaptions": c["esconde"],
            "texts": c["textos"],
        })
        print("cena: %-26s %4.1fs  %d parametros" % (c["id"], c["dur"], len(par)))

    cat = os.path.join(AQUI, "catalog.martires.json")
    with open(cat, "w", encoding="utf-8") as f:
        json.dump({"version": "martires-1", "scenes": entradas}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("\n%d cenas em %s" % (len(entradas), SAIDA))
    print("catalogo em %s" % cat)


if __name__ == "__main__":
    construir()
