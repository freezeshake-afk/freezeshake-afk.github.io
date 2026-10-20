# Prompts prontos para o Google Flow — avatar de podcast

Avatar estilo podcast contando histórias de mártires. Tudo aqui é pra copiar e
colar. Dois roteiros completos: **Estêvão** (9 clipes) e **Policarpo** (9 clipes).

---

## Passo 1 — gerar a imagem mestre

Gere **uma** imagem e use ela como primeiro frame de **todos** os clipes. É o que
mantém o avatar idêntico. Não gere uma imagem por clipe — isso quebra a
consistência, que é justamente o problema que a imagem resolve.

### Prompt da imagem mestre

```
Retrato fotográfico de um homem brasileiro de 34 anos sentado em um estúdio
de podcast escuro. Pele clara, barba curta castanha bem aparada, cabelo
castanho escuro curto penteado para trás, olhos castanhos, sobrancelhas
marcadas. Camiseta preta lisa de gola redonda.

Ele está sentado em uma cadeira de couro preto, levemente inclinado para a
frente, cotovelos apoiados na mesa, olhando direto para a câmera com
expressão séria e intensa.

Estúdio escuro: parede de fundo em painéis acústicos cinza-escuro,
desfocada. Uma luz quente âmbar vem de cima à esquerda e desenha o contorno
do rosto; uma segunda luz fraca azulada vem de trás à direita, separando ele
do fundo. Clima noturno, contrastado, cinematográfico.

Um microfone de podcast preto sobre braço articulado entra pela borda
inferior direita do quadro, abaixo da linha do queixo, sem cobrir o rosto.

Enquadramento vertical 9:16. Plano médio-fechado: cabeça e ombros, rosto no
terço superior do quadro, com folga acima da cabeça. Altura dos olhos, lente
35mm, foco nítido no rosto, fundo desfocado.

Fotorrealista, pele com textura natural, sem retoque excessivo.
Sem texto, sem legenda, sem logotipo, sem marca d'água.
```

### Por que essas escolhas

| escolha | motivo |
|---|---|
| microfone na borda inferior, abaixo do queixo | o card do modo board recorta uma faixa em torno de **34% da altura**; microfone no meio tampa o rosto |
| rosto no terço superior com folga | sem folga, a cabeça encosta na borda do card |
| fundo escuro com âmbar | é o mesmo esquema das 6 cenas do pacote, então o avatar e os painéis combinam |
| camiseta preta lisa | roupa com estampa muda de clipe pra clipe e denuncia o corte |
| sem texto na imagem | o editonny queima a legenda dele; texto aqui vira legenda dupla |

Se quiser variação, gere **no máximo 2 variantes** mudando só o ângulo
(levemente de lado, levemente mais fechado) e mantendo tudo o mais igual.
Use a mestre na maioria dos clipes.

---

## Passo 2 — gerar os vídeos

No Flow, use o caminho de **imagem → vídeo**: a imagem mestre como primeiro
frame, e um dos prompts abaixo como instrução de movimento e fala.

Como a identidade já vem da imagem, o prompt do vídeo fica curto. Ele só precisa
dizer **como entrega**, **o que fala** e **o que não fazer**.

### Bloco fixo

Vai no fim de todo prompt de vídeo, sempre igual:

```
Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

> Os prompts abaixo já trazem esse bloco embutido. É só copiar o bloco inteiro
> de cada clipe.

---

# ESTÊVÃO — 9 clipes

Roteiro em [`estevao.md`](estevao.md) · fonte: Atos 6–8

### Clipe 01 — gancho

```
O homem olha direto para a câmera e aponta o dedo indicador para a lente.
Ele diz, exatamente estas palavras: "A Bíblia mostra Jesus sentado no trono
do Pai. Tem um único momento em que ela mostra ele de pé."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 02 — quem

```
O homem abre as duas mãos na frente do peito, palmas para cima.
Ele diz, exatamente estas palavras: "Jerusalém, ano trinta e quatro. Um
rapaz chamado Estêvão é arrastado pro tribunal religioso mais poderoso do
país."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 03 — a acusação

```
O homem encolhe os ombros com as palmas das mãos viradas para cima.
Ele diz, exatamente estas palavras: "Acusaram ele com testemunha falsa. E em
vez de se defender, Estêvão faz um sermão de quase meia hora."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 04 — a provocação

```
O homem bate a mão aberta na outra palma, uma vez, marcando a frase.
Ele diz, exatamente estas palavras: "E termina chamando os juízes de
obstinados, dizendo que eles sempre resistem ao Espírito Santo. Eles
rangeram os dentes de raiva."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 05 — a visão

```
O homem leva a mão ao peito, expressão de assombro contido.
Ele diz, exatamente estas palavras: "Aí Estêvão olha pra cima e fala: vejo
os céus abertos, e o Filho do Homem em pé à direita de Deus."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 06 — o linchamento

```
O homem balança a cabeça negando devagar, com pesar.
Ele diz, exatamente estas palavras: "Eles taparam os ouvidos, arrastaram ele
pra fora da cidade e começaram a apedrejar. E deixaram os casacos aos pés de
um jovem."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 07 — a oração

```
O homem aproxima as duas mãos até quase se tocarem, voz baixando de
intensidade sem perder a urgência.
Ele diz, exatamente estas palavras: "De joelhos, sangrando, ele orou:
Senhor, não os consideres culpados deste pecado. E morreu ali."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 08 — a virada dupla

```
O homem aponta o dedo indicador para a lente, sobrancelhas levantadas,
expressão de revelação.
Ele diz, exatamente estas palavras: "Jesus tava de pé pra receber ele. E o
jovem que guardou os casacos? Chamava Saulo. Virou o apóstolo Paulo."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

### Clipe 09 — fecho

```
O homem abre as duas mãos na frente do peito, sorriso leve, tom de convite.
Ele diz, exatamente estas palavras: "Comenta amém se você não sabia dessa.
Amanhã tem outra."

Entrega: fala rápida, intensa e urgente, como quem conta uma história que
não pode esperar. Olha direto na lente o tempo todo. Sobrancelhas ativas.
Nunca faz pausa longa, nunca desvia o olhar. Português brasileiro coloquial.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudança de roupa, cenário ou iluminação.
```

---

# POLICARPO — 9 clipes

Roteiro em [`GUIA-ROTEIRO-E-FLOW.md`](GUIA-ROTEIRO-E-FLOW.md) · fonte:
*Martírio de Policarpo*

Mesmo bloco fixo. Só a primeira linha e a fala mudam.

| clipe | gesto | fala exata |
|---|---|---|
| 01 | aponta o dedo indicador para a lente | "Esse homem tinha oitenta e seis anos. Ofereceram a vida dele de volta por três palavras. Ele olhou pro governador e disse não." |
| 02 | abre as duas mãos na frente do peito | "O nome dele era Policarpo, bispo de Esmirna. E ele não era um cara qualquer: ele tinha sido discípulo do apóstolo João." |
| 03 | leva a mão ao peito | "Ano cento e cinquenta e cinco. Cidade de Esmirna, na província romana da Ásia. Hoje isso é a Turquia." |
| 04 | encolhe os ombros com as palmas para cima | "Vieram buscar ele de madrugada. E sabe o que ele fez? Mandou servir comida pros soldados que vinham prender ele." |
| 05 | aproxima as duas mãos até quase se tocarem | "No estádio lotado, o procônsul ofereceu a saída mais fácil do mundo: jura pelo imperador, amaldiçoa o Cristo, e você vai pra casa." |
| 06 | levanta um dedo indicando "primeiro" | "Oitenta e seis anos. Era esse o tempo que ele já servia a Cristo quando pediram pra ele negar tudo numa tarde." |
| 07 | bate a mão aberta na outra palma, uma vez | "E ele respondeu: oitenta e seis anos eu o sirvo, e ele nunca me fez mal algum. Como posso blasfemar do meu Rei, que me salvou?" |
| 08 | balança a cabeça negando devagar | "Levantaram a fogueira. E quando foram pregar ele na estaca, ele pediu pra só amarrarem. Disse que quem dava força pra ficar no fogo ia sustentar ele sem os pregos." |
| 09 | aponta o dedo indicador para a lente | "Dois mil anos depois a gente ainda tá falando dele. Comenta amém se essa te marcou, e segue que amanhã tem outra." |

Monte assim:

```
O homem <GESTO DA TABELA>.
Ele diz, exatamente estas palavras: "<FALA DA TABELA>"

<BLOCO FIXO>
```

> O clipe 08 do Policarpo é o mais longo (31 palavras). Se não couber em 8
> segundos, corte para: *"Levantaram a fogueira. Quando foram pregar ele na
> estaca, ele pediu pra só amarrarem — quem dava força pro fogo ia sustentar
> ele sem os pregos."*

---

## Passo 3 — nomear e mandar

Salve **na ordem da narrativa**, com zero à esquerda:

```
01.mp4  02.mp4  03.mp4  ...  09.mp4
```

A ordem alfabética é a ordem da montagem. `1.mp4` e `10.mp4` saem fora de
ordem — por isso o zero.

**Não junte os clipes antes de mandar.** Mande os 9 separados.

A edição precisa saber onde cada clipe começa e termina para emendar o áudio
sem estalo, encaixar as cenas na fronteira certa e cortar as sobras de início
e fim de cada geração. Num arquivo só, essa informação se perde e a montagem
fica pior.

Se já tiver juntado, manda assim mesmo que dá pra trabalhar — só sai um pouco
menos preciso.

---

## Checklist antes de gerar os 9

Gere **um** clipe primeiro e confira:

- [ ] a fala saiu **exatamente** como no roteiro, sem o modelo inventar palavra
- [ ] coube nos 8 segundos sem cortar no meio de uma frase
- [ ] **não** apareceu legenda nem texto na tela
- [ ] **não** veio música de fundo, só a voz
- [ ] a câmera ficou parada
- [ ] o rosto está no terço superior, com folga acima da cabeça
- [ ] o microfone não cobre o queixo nem a boca

Se a fala não bateu, repita o trecho `Ele diz, exatamente estas palavras:` e
encurte a frase. Se veio legenda, reforce `sem legenda, sem texto na tela` no
começo **e** no fim do prompt.

Só depois que um clipe passar no checklist é que vale gerar os outros oito.
