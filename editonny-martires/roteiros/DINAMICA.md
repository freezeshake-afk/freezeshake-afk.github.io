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


---

## v3: o que mudou

### Cortar o ar morto vale mais que qualquer efeito

Os clipes do Flow vêm com silêncio nas bordas: a fala começa depois que o clipe
começa e acaba antes de ele terminar. No Estêvão eram **5,66 s em 70 s — 8% do
vídeo**. Medindo a envoltória de energia de cada janela de 10 s e recortando com
0,08 s de respiro na entrada e 0,14 s na saída, o vídeo caiu para 65,9 s e cada
emenda passou a estalar.

Faça isso **antes** de posicionar qualquer coisa.

### Ancore em palavra, não em segundo

Depois de reapertar o corte, todo tempo absoluto quebra. A solução é anotar o
plano em cima do roteiro alinhado:

```python
ZOOMS = [("assassinato", 1.34, None, 0.13, "whoosh"), ...]
TRANSICOES = [("transition-flash", round(t("apedrejar") + 0.05, 2)), ...]
```

Assim o plano sobrevive a recorte, regeração de clipe e troca de take.

### Três recursos novos

- **`text-two-line-title`** no gancho: linha pequena em cima, linha grande em
  âmbar embaixo. Vale mais que legenda normal nos primeiros 3 segundos.
- **`text-pop`** no pico: legenda de 2 palavras gigantes com a última em cor de
  destaque. É uma cena de legenda, então usa as palavras reais do roteiro.
- **`text-impact`** na virada: frase em duas linhas com halo.

### Armadilha: parâmetro documentado que não funciona

A cena `text-impact` declara o parâmetro **`glow`**, mas o código lê
**`P.sparkle`**, que não existe no bloco `var P` — então ele cai no verde padrão
e o botão documentado não faz nada. Até achar, o halo saía verde num vídeo
âmbar.

Contorno: renomeie a chave no bloco da cópia:

```python
if "sparkle:" not in c:
    c = c.replace("\n    glow:", "\n    sparkle:", 1)
```

Vale conferir o `var P` da cópia contra o que o código realmente lê sempre que
um parâmetro parecer ignorado.

### E uma de bom senso

`martir-contador` com `valor: 1` e `de: 0` passa a maior parte da animação
mostrando **0**. Contar até 1 não faz sentido: use `de: 1`.


---

## O que dois virais de referência ensinam (medido)

Dois vídeos de política brasileira usados como referência de edição. Medi em vez
de achar, e o resultado contraria o instinto.

| | referência A | referência B | meu v3 |
|---|---|---|---|
| duração | 2min39 | 4min12 | 1min06 |
| cortes | 1 a cada **7,9 s** | 1 a cada **3,9 s** | 4 trocas de painel |
| eventos de edição | poucos | quase nenhum | 1 a cada 2,3 s |
| legenda | caixa alta pequena + gráficos | **frase minúscula**, y 0,586 | CAIXA ALTA, y 0,748 |
| música | nenhuma | nenhuma | trilha baixa |

### 1. Eles são mais calmos, não mais agitados

A corta a cada 8 segundos. Nenhum dos dois tem motion graphics constante. O que
segura não é efeito, é **densidade de informação** — eles entregam fato atrás de
fato sem respiro de conteúdo.

Conclusão desconfortável: dinamismo visual tem teto, e eu provavelmente passei
dele no v3.

### 2. A legenda deles é legível, não decorativa

A referência B usa **frase inteira em caixa baixa, duas linhas, centro em 0,586
da altura** — bem mais alta que a minha (0,748) e com cobertura de 92% do tempo,
trocando a cada ~1,5 s.

É um visual de documentário, não de viral de nicho. Para histórias de mártires
isso provavelmente cai melhor que o bloco de 2-3 palavras em caixa alta.

Para trocar, no `project.json`:

```json
"captions": {"enabled": true, "style": "standard", "maxWords": 6, "inFrame": true}
```

e suba a posição. Vale testar as duas versões do mesmo vídeo.

### 3. Prova em vez de gráfico

Entre 10 s e 15 s, a referência B emenda **oito clipes de outras pessoas** —
vídeos comuns de rede social, cada um com meio segundo, legendas originais à
mostra. É um muro de vozes como prova social.

O equivalente honesto no nicho de mártires não é vídeo de terceiros: é **a
fonte**. Versículo na tela, página do relato, mapa, ícone antigo. É o papel que
as cenas do pacote já cumprem — e sugere usar mais delas, não mais efeito.

### 4. A fala

O apresentador das duas referências não é acelerado. Ele é **firme e
articulado**: segura o olhar, gesticula sem parar com as mãos abertas perto do
peito, e marca a palavra importante com uma **pausa curta antes dela**, não
levantando a voz.

Isso muda o bloco de entrega dos prompts do Flow. A versão nova está em
[`andre.md`](andre.md); a antiga pedia "fala rápida e intensa", que puxa para o
lado errado.

### 5. Duração

Os dois passam de 2 minutos. Não quer dizer que vídeo longo viraliza — quer
dizer que **o limite não é o relógio, é o conteúdo**. Se a história tem fato
novo a cada frase, ela sustenta. Se tem enchimento, 60 s já é longo.
