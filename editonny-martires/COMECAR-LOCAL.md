# Continuar numa conversa local

Este arquivo passa o contexto de uma sessão na nuvem para uma sessão do Claude
Code rodando no seu PC. Cole a mensagem de abertura e siga.

---

## 1. Mensagem de abertura

Abra o terminal na pasta do repositório, rode `claude`, e cole isto:

```
Leia editonny-martires/COMECAR-LOCAL.md e editonny-martires/README.md antes
de qualquer coisa. É a continuação de um trabalho que vinha de outra sessão.

Resumo: eu faço Reels de histórias de mártires cristãos para o Instagram.
O avatar é gerado no Google Flow, e a edição é feita com o editonny mais um
pacote de 6 cenas próprias que está neste repositório.

Primeira tarefa: rode editonny-martires/preparar.py e me diga o que falta
instalar na minha máquina.
```

---

## 2. O que já existe

Repositório `freezeshake-afk/freezeshake-afk.github.io`, branch
**`claude/editor-reels-martires`** (ainda não mesclada na `main`).

```
git clone https://github.com/freezeshake-afk/freezeshake-afk.github.io
cd freezeshake-afk.github.io
git checkout claude/editor-reels-martires
```

### `editonny-martires/` — o que importa

| arquivo | o que é |
|---|---|
| `preparar.py` | confere os requisitos do PC e diz o comando exato do que falta |
| `instalar.py` | integra as 6 cenas ao editonny; **rode de novo a cada update dele** |
| `construir.py` | gera os HTML das cenas; é aqui que se mexe no visual, nunca no HTML |
| `validar.py` | renderiza as cenas no motor real e salva um frame de cada |
| `scenes/*.html` | as 6 cenas (geradas — não editar na mão) |
| `roteiros/PROMPTS-FLOW.md` | prompt da imagem mestre + 18 prompts de vídeo |
| `roteiros/estevao.md` | roteiro de Estêvão + calendário de 39 vídeos |
| `roteiros/GUIA-ROTEIRO-E-FLOW.md` | prompt mestre, fórmula de gancho, roteiro de Policarpo |

### `martires-reels/` — pipeline alternativo

Editor próprio em ffmpeg + Python, feito antes de descobrir o editonny. Está
superado para uso normal, **mas** alinha legenda sem Whisper (por energia do
áudio, usando o roteiro conhecido). Serve quando não dá para baixar o modelo.
O `tema.json` dele guarda as medições do vídeo de referência.

---

## 3. Estado real

**Nada que foi instalado na sessão da nuvem existe no seu PC.** O container era
descartável. No PC é instalação do zero:

1. `python3 editonny-martires/preparar.py` → lista o que falta
2. instalar o que faltar
3. `git clone https://github.com/soumatheusgomes/editonny` e
   `python3 install.py --target both`
4. `cd editonny-martires && python3 instalar.py`
5. conferir: `preparar.py` tudo verde, e o `doctor` do editonny dizendo
   **151 scenes; 0 missing files**

O que **está** pronto e versionado: as 6 cenas, validadas no `lint` e no
`check` do HyperFrames, os roteiros e os prompts.

O que **não** está feito: nenhum vídeo real foi produzido ainda. O
`preview/contato.png` mostra as cenas com vídeo sintético de teste no lugar do
avatar.

---

## 4. Requisitos — os que pegam

| item | versão | pegadinha |
|---|---|---|
| Python | 3.9+ no lançador, **>=3.10 e <3.14** no engine | **3.14 quebra**; o uv contorna baixando uma compatível |
| Node.js | **22.13+ ou 24+** | versão antiga falha no render |
| uv, FFmpeg, ffprobe | qualquer | — |
| OCR | Tesseract com **`por`** e `eng`, ou Apple Vision no macOS | só `eng` não serve para conteúdo em português |
| disco | ~5 GB | pacote 1,1 GB + navegador 365 MB + modelo |

**No Windows:** o instalador do editonny usa link simbólico, que é restrito sem
**Modo de Desenvolvedor** ligado. O `preparar.py` testa isso criando um link de
verdade. A documentação do editonny diz que ele é validado em macOS Apple
Silicon e que Windows e Linux precisam de validação própria.

---

## 5. Regras que custaram caro

Não redescubra estas. Elas vieram de erro real com o `check` do motor
reprovando.

### Ao mexer nas cenas

1. **Nunca monte nome de classe no JavaScript.** O `apply.py` do editonny
   renomeia identificadores para cada cópia de cena ser independente. Uma
   string como `className = "t-marco" + (...)` ele trata como prefixo de ID
   dinâmico: reescreve a string no JS e **não** o `.t-marco` do CSS. A classe
   para de casar e a cena desmonta — aconteceu com a linha do tempo. Por isso
   tudo é estático: elementos no HTML com IDs literais, e o JS só preenche
   texto e posição.
2. **Nada de `scale` nas animações.** O renderizador não aceita; o helper
   `lim()` converte `scaleX`/`scaleY` em `clip-path`. Use opacidade, `x`/`y`,
   `rotation` e `clipPath`.
3. **Edite `construir.py`, nunca os HTML.** Os HTML são gerados e qualquer
   mudança neles se perde no próximo `construir.py`.
4. Depois de mexer: `construir.py` → `instalar.py` → `validar.py`.

O `check` do HyperFrames é QA de verdade: pega texto sobreposto, contraste
WCAG AA e oclusão. Quando a sobreposição for de propósito, marque com
`data-layout-allow-occlusion`.

### Ao gerar no Flow

Medições do vídeo de referência (720x1280, normalizadas) que ditam o
enquadramento:

- o card do modo board recorta uma faixa em torno de **34% da altura** → rosto
  no terço superior, com folga acima, e microfone abaixo do queixo
- legenda em maiúsculas, blocos de 2–3 palavras, altura de maiúsculas de 42px
  em 1080 de largura
- fala contínua, sem pausa: não há silêncio nem a −45dB na referência
- fundo quase preto com grade de 90px e brilho âmbar no topo

E no prompt do Flow, sempre: **sem legenda** (senão fica legenda dupla), **sem
música** (briga com a trilha e piora a transcrição), **sem corte** e **sem
movimento de câmera**.

---

## 6. Quando os clipes chegarem

Clipes separados, nomeados `01.mp4` … `09.mp4` numa pasta só. Não concatene
antes — a edição precisa das fronteiras para emendar o áudio e encaixar as
cenas.

```
/editonny
Edita esse vídeo. Os clipes estão em <PASTA>, na ordem dos nomes.
É sobre <MÁRTIR>. Roteiro em editonny-martires/roteiros/<arquivo>.md.
Dinâmico e agitado, legenda queimada de 2 a 3 palavras, trilha baixa.
Usa as cenas de mártires nos pontos marcados no roteiro.
```

O editonny mostra um card de configurações e **espera você responder ok** antes
de editar. Entrega em `Downloads/editonny/<data>-<nome>/exports/`.

---

## 7. Decisões já tomadas

Para a sessão local não reabrir:

- **editonny em vez do `martires-reels`** — ele faz tudo e mais (145 cenas,
  transcrição, limpeza automática, trilha, revisão por amostra)
- **Electron foi descartado** — a interface do editonny é a conversa; um app de
  desktop obrigaria a reconstruir o agente. Se um dia fizer sentido uma tela,
  é uma página HTML local para preencher os parâmetros das cenas, não Electron
- **avatar de podcast gerado por imagem→vídeo**, com uma imagem mestre reusada
  como primeiro frame de todos os clipes
- **escrever das fontes primárias**, não do livro *Loucos por Jesus* — ele é
  todos os direitos reservados, e parafrasear de perto continua sendo obra
  derivada. O índice dele (nomes, lugares, datas) é fato e pode guiar a pauta;
  o texto vem de Atos, Eusébio, do *Martírio de Policarpo*, da *Paixão de
  Perpétua*, das cartas de Inácio e do Foxe — todos domínio público

---

## 8. Conteúdo: conferir antes de publicar

Datas de martírio são disputadas. Policarpo aparece como 155 e como 168;
Blandina costuma ser 177; Telêmaco varia entre 391 e 404. A fonte do Policarpo
não cita ano de calendário, só o dia e o procônsul.

Isso pesa porque a cena `martir-contador` põe o número gigante no meio da tela.
Quando a data não for firme: diga "por volta de", ou troque pelo detalhe que a
fonte afirma direto ("no reinado de Marco Aurélio"), que é mais forte e não
erra.
