# Dinâmica: como deixar o vídeo mais agitado

O editonny já traz a biblioteca de efeitos pronta — **não precisa construir nada
com Remotion**. São 10 transições, 13 efeitos de vídeo, 17 ponteiros, 9 entradas
de imagem e 19 tratamentos de legenda e título, todos no catálogo.

Além disso o motor tem o recurso que mais rende por esforço: **zoom de impacto
por bloco**, que é o "zoom digital" feito nativamente.

---

## 1. Zoom de impacto (o que mais rende)

Dentro de um bloco `fullscreen` do `project.json`:

```json
{"scene": "fullscreen", "start": 0, "end": 9.8, "zoom": 1.0,
 "zooms": [
   {"at": 5.79, "scale": 1.18, "end": 6.90, "sound": "none"},
   {"at": 8.09, "scale": 1.32, "duration": 0.14}
 ]}
```

- `at` — segundos do corte **ou uma palavra falada**; a palavra é mais robusta
  porque sobrevive a mudança de tempo
- `scale` — 1.12 é sutil, 1.30 é um soco; acima de 1.4 o vídeo amolece
- `end` — devolve o enquadramento; sem `end` o zoom fica até o fim do bloco
- `duration` — 0.12 a 0.15 dá o corte seco; 0.45 dá movimento suave
- `sound` — padrão é `whoosh`; use `"none"` nos zooms pequenos para não poluir

Só funciona em bloco `fullscreen` (ou `evidence`), e não combina com ponteiros
(`overPerson`) no mesmo bloco.

## 2. Transições

Aplicadas no instante do impacto, não no intervalo:

```
python3 <EDITONNY>/visuals/apply.py --project PROJ --use transition-film-burn --cut 9.3
```

`glow` (0,4s) · `flash` (0,3s) · `film-burn` (0,6s) · `glitch` (0,4s) ·
`tv` (0,6s) · `curtain` (0,6s) · `zoom` (0,5s) · `blinds` (0,6s) ·
`iris` (0,7s) · `fade` (0,5s)

> **Cuidado:** a transição precisa terminar **antes** de a moldura começar a
> fechar, senão cobre o rosto durante a animação do quadro. Com `ANTES = 0.8`,
> corte a transição ~0,5 s antes do início do bloco `frame`.

## 3. Efeitos de vídeo

```
apply.py --project PROJ --use effect-cinema --start 30.9 --end 33.7
```

`cinema` (letterbox de trailer) · `noir` (monocromático) · `vignette` ·
`glow` · `blur` · `chromatic-blur` · `shake` · `prism` · `tv-lines` ·
`static` · `vhs` · `money-rain` · `confetti`

---

## O que serve ao nicho de mártires

Nem todo efeito cabe. A história é a morte de uma pessoa real; efeito de
marketing a barateia.

| usar | evitar |
|---|---|
| `film-burn`, `glow`, `flash`, `iris`, `fade` | `money-rain`, `confetti` |
| `cinema`, `noir`, `vignette`, `shake` | `vhs`, `tv-lines`, `glitch` |
| zoom de impacto nas palavras-chave | `text-twist`, `text-doodle`, `color-glitch` |
| `pointer-circle` e `underline` numa citação | mockup de celular, capa de revista |

A regra: o efeito marca **o que a frase está dizendo**. Flash na primeira
pedra, glow na redenção, vinheta no peso. Efeito que só enfeita, tira.

---

## O que foi usado no Estêvão

16 eventos em 70 s, cerca de um a cada 4 s, além dos 4 painéis:

| tempo | evento | por quê |
|---|---|---|
| 5,8s | zoom 1.18 em "de pé" | marca a palavra do gancho |
| 8,1s | zoom 1.32 em "assassinato" | soco antes da virada |
| 9,3s | `transition-film-burn` | muda de assunto |
| 30,4s | zoom 1.24 em "rangeram" | a fúria |
| 30,9–33,7s | `effect-cinema` | "olha pra cima": revelação |
| 32,2s | `transition-zoom` | mergulha na visão |
| 44,4s | zoom 1.28 + `transition-flash` + `effect-shake` | a primeira pedra |
| 48,0–50,6s | `effect-vignette` | o peso antes da oração |
| 50,0s | zoom 1.14 em "de joelhos" | aproxima na morte |
| 50,4s | `transition-glow` | entra a oração |
| 60,1–62,9s | `effect-glow` | "Jesus tava de pé pra receber ele" |
| 63,7s | zoom 1.30 em "Saulo" | a revelação dupla |
| 66,6s | zoom 1.12 | fecha no CTA |
| 69,2s | `transition-iris` | encerra |

Sons de efeito ficaram **desligados** nesta versão (`apply.py --sounds` adiciona
os 15 sugeridos). Com whoosh em todo zoom o vídeo fica barulhento; vale testar
ligando só nos dois ou três maiores.
