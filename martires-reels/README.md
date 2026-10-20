# martires-reels

> **Leia antes:** o vídeo de referência foi editado com o
> [editonny](https://github.com/soumatheusgomes/editonny), que faz tudo o que este
> pipeline faz e muito mais (145 cenas, transcrição, limpeza automática de pausas e
> erros, trilha, revisão por amostra). Para o nicho de mártires, veja
> [`editonny-martires/`](../editonny-martires/) neste mesmo repositório.
>
> Este pipeline continua aqui porque é simples, roda só com ffmpeg + Python e é
> todo seu para mexer. As medições do vídeo de referência em `tema.json` também
> valem como documentação do estilo.


Editor automático de Reels no estilo do vídeo de referência, para o nicho de
**mártires cristãos**. Você gera os clipes do seu clone no **Google Flow**,
escreve o roteiro com marcadores, e o programa monta o vídeo final pronto pro
Instagram.

O que ele faz sozinho:

- junta os clipes do Flow num vídeo só (9:16, 1080x1920, 30fps);
- **legenda queimada** em blocos de 2–3 palavras, caixa alta, com "pop" na entrada;
- alterna entre **modo cheio** (você em tela cheia) e **modo board** (fundo escuro
  com grade, brilho laranja no topo e você num card arredondado com borda luminosa);
- desenha **pílulas de tópico** e **cards de citação** com animação de entrada;
- mistura a **trilha** com ducking automático (a música abaixa quando você fala);
- normaliza o áudio em **-14 LUFS**, que é o padrão do Instagram.

Todo o visual saiu de medição pixel a pixel do vídeo de referência — posição e
tamanho da legenda, geometria do card, altura e cor da pílula, espaçamento da
grade. Os números estão em `tema.json` com o comentário `_medido`.

---

## Instalação

Precisa de `ffmpeg` (com libass), Python 3.10+ e Chromium.

```bash
sudo apt install ffmpeg fonts-inter
pip install pyyaml pillow numpy faster-whisper
npx playwright install chromium      # usado pra desenhar as artes
```

Se a fonte Inter não estiver disponível, troque `legenda.fonte` no `tema.json`
por outra que você tenha instalada.

---

## Uso

```bash
# 1. jogue os clipes do Flow em clipes/ (a ordem é alfabética: 01, 02, 03...)
# 2. escreva o roteiro em roteiros/
python3 reel.py roteiros/policarpo.txt
```

Sai em `out/policarpo.mp4`.

Opções:

| flag | pra que serve |
|---|---|
| `--clipes a.mp4 b.mp4` | escolhe os clipes na mão (ou passa uma pasta) |
| `--musica trilha.mp3` | trilha de fundo |
| `--out video.mp4` | nome do arquivo final |
| `--sem-whisper` | alinha a legenda pela energia do áudio, sem baixar modelo |
| `--modelo medium` | modelo do Whisper (`tiny`/`base`/`small`/`medium`) |
| `--zoom` | zoom lento no modo cheio |
| `--so-legendas` | gera só o `.ass` pra você conferir antes de renderizar |

---

## O roteiro

Um `.txt` com um cabeçalho e o texto da narração. Os **marcadores** entre
`[[ ]]` ficam no meio do texto — o tempo de cada um sai da palavra que vem logo
depois, então você não precisa cronometrar nada.

```
---
titulo: Policarpo - o bispo que nao negou
arquivo: policarpo
clipes: [../clipes]
musica: ../assets/musica/epico.mp3
---

[[pilula: 🔥 | esmirna, ano 155]]
No ano cento e cinquenta e cinco, um homem de oitenta e seis anos
foi arrastado para o meio do estadio.
[[/pilula]]

[[board]]
[[card: ✝️ | 86 ANOS SERVINDO A <<CRISTO>> | e pediram que ele negasse tudo | policarpo de esmirna]]
O nome dele era Policarpo, discipulo do apostolo Joao.
[[/card]]

[[cheio]]
E ele nao negou.
```

### Marcadores

| marcador | efeito |
|---|---|
| `[[cheio]]` | volta pra tela cheia |
| `[[board]]` | entra no fundo escuro com você no card |
| `[[pilula: ÍCONE \| texto]]` | pílula no topo (ícone pode ser emoji) |
| `[[pilula: 2 \| texto]]` | se o primeiro campo for número, vira bolinha numerada |
| `[[card: ÍCONE \| título \| subtítulo \| tag]]` | card grande na parte de cima |
| `[[/pilula]]` `[[/card]]` | tira da tela (senão some sozinho em ~4s / ~5s) |

No título do card, `<<palavra>>` sai com o gradiente rosa-pêssego da referência.
Campos do meio podem ficar vazios: `[[card: | SÓ O TÍTULO]]`.

---

## Como as legendas são sincronizadas

1. **Whisper** (padrão): transcreve o áudio do seu clone com tempo por palavra e
   casa com o texto do roteiro. É o modo preciso — use este na sua máquina.
2. **Energia** (`--sem-whisper`): distribui as palavras do roteiro pela energia
   do áudio, contando sílabas. Não baixa nada e funciona offline, mas só acerta
   se o roteiro for fiel ao que foi falado.

O casamento é por similaridade, então pequenas diferenças entre o roteiro e o que
o clone falou não quebram a sincronia.

---

## Ajustar o visual

Tudo em `tema.json`. Os que mais mudam o resultado:

- `legenda.tamanho_cheio` / `tamanho_board` — **74** = altura de maiúsculas de
  42px em 1080 de largura, igual à referência;
- `legenda.y_cheio` **0.748** e `y_board` **0.487** — altura da legenda na tela;
- `pip.x/y/w/h` — posição e tamanho do seu card no modo board;
- `pip.zoom` — acima de 1 aperta o enquadramento do rosto dentro do card;
- `fundo.glow_topo` e `fundo.grid_px` — o brilho laranja e a grade do fundo;
- `musica.volume_db` e `ducking_db` — o quanto a trilha abaixa quando você fala.

As artes são HTML em `templates/` — mexer no CSS muda o desenho dos cards e
pílulas direto, sem tocar em código.

---

## Testar sem gastar crédito do Flow

```bash
python3 ferramentas/clipes_teste.py --n 11 --dur 8 --saida clipes
python3 reel.py roteiros/policarpo.txt --sem-whisper
```

Gera clipes 9:16 falsos com cadência de fala, só pra ver o layout funcionando.

---

## Fluxo de trabalho sugerido

1. escreve o roteiro inteiro primeiro (é ele que define o ritmo);
2. gera no Flow os clipes do clone falando, na ordem, com nomes `01.mp4`, `02.mp4`...;
3. roda `--so-legendas` e confere o `.ass` em `build/`;
4. roda o render completo;
5. se algum card ficou no tempo errado, move o marcador uma ou duas palavras no
   roteiro e roda de novo.

## Estrutura

```
reel.py                 CLI
tema.json               todo o visual (medido da referência)
core/roteiro.py         lê o roteiro e os marcadores
core/alinhar.py         Whisper + fallback por energia
core/legendas.py        gera o .ass
core/artes.py           HTML -> PNG (Chromium) + máscara do PiP
core/render.py          monta tudo no ffmpeg
templates/              HTML/CSS das artes
ferramentas/            gerador de clipes de teste
clipes/ out/ build/     entrada, saída e arquivos intermediários
```
