# André — Patras, Acaia, c. 66 d.C.

**Fontes:** João 1.35-42 (o chamado e o gesto), João 6.8-9 e 12.20-22 (as outras
duas aparições), Eusébio *HE* 3.1 citando Orígenes (Cítia), *Atos de André*
(séc. II) e a *Paixão de André* (martírio em Patras).

**Alvo:** 8 clipes de 10s · 180 palavras · ~80s

---

## O ângulo

André é sempre "o irmão de Simão Pedro". Mas em João ele é chamado **primeiro**,
e a primeira coisa que faz depois de encontrar Jesus é ir buscar o irmão. O
apóstolo mais famoso da história existe por causa do que ninguém lembra.

O gancho é essa inversão. O fecho paga ela.

---

## ⚠️ Antes de gravar: a cruz em X não serve

A "cruz de Santo André" em formato de X é **tradição tardia**, medieval. Os
relatos antigos não dizem isso. O que a *Paixão de André* registra é que ele foi
**amarrado**, não pregado, justamente para demorar a morrer — e que ficou dois
dias falando com a multidão.

Esse detalhe é mais forte que o X e é o que a fonte sustenta. O roteiro abaixo
usa o amarrado. **Não ponha um X na tela.**

A data (c. 66) é tradicional, não documentada. Na tela, prefira "por volta de".

---

## Roteiro

**Clipe 1 — gancho**
*"Todo mundo conhece Pedro. Quase ninguém sabe o nome do irmão que levou o
Pedro até Jesus. E esse irmão foi chamado primeiro."*
Gesto: abre as duas mãos na frente do peito, palmas para cima

**Clipe 2 — quem** → `martir-ficha`
*"O nome dele era André. Pescador da Galileia, discípulo de João Batista. No
evangelho de João, ele é o primeiro a seguir Jesus."*
Gesto: leva a mão ao peito

**Clipe 3 — o gesto** → `martir-ultimas-palavras`
*"E a primeira coisa que ele faz depois de encontrar o Messias é ir atrás do
irmão. Achamos o Cristo, ele diz, e leva o Pedro."*
Gesto: aponta o indicador para a lente

**Clipe 4 — a sombra**
*"Depois disso, André some do centro da história. Pedro vira a pedra. E André
aparece só três vezes, sempre levando alguém até Jesus."*
Gesto: encolhe os ombros com as palmas para cima

**Clipe 5 — onde acabou** → `martir-local`
*"A tradição diz que ele pregou até a Grécia e acabou preso em Patras, por
ordem do governador romano."*
Gesto: aproxima as duas mãos até quase se tocarem

**Clipe 6 — a cruz**
*"Condenaram ele à cruz. E segundo o relato mais antigo, não pregaram:
amarraram. Pra morrer devagar, de sede e de exaustão."*
Gesto: balança a cabeça negando devagar

**Clipe 7 — os dois dias** → `martir-contador`
*"Ele levou dois dias pra morrer. E usou os dois dias pregando pra multidão que
tinha vindo assistir ele morrer."*
Gesto: bate a mão aberta na outra palma, uma vez

**Clipe 8 — fecho**
*"O primeiro a ser chamado foi o último a ser lembrado. Comenta o nome dele aqui
embaixo. Amanhã tem outra."*
Gesto: aponta o indicador para a lente

---

## Parâmetros das cenas

```
martir-ficha                      (clipe 2)
  nome: "André"
  anos: "morto por volta de 66 d.C."
  cidade: "Patras, província da Acaia"
  nota: "irmão de Pedro, o primeiro chamado"

martir-ultimas-palavras           (clipe 3)
  citacao: "Achamos o Messias|— e levou o irmão|até Jesus."
  autor: "André, sobre Simão Pedro"
  fonte: "João 1.41-42"

martir-local                      (clipe 5)
  cidade: "PATRAS"
  provincia: "província romana da Acaia"
  ano: "c. 66 d.C."
  nota: "hoje Pátra, na Grécia"

martir-contador                   (clipe 7)
  valor: 2 · de: 0 · unidade: "dias"
  rotulo: "AMARRADO NA CRUZ"
  nota: "e passou os dois pregando"
```

> O contador aqui conta mesmo (0 → 2), diferente do Estêvão onde o valor era 1.

---

## Prompts do Flow

Mesma imagem mestre do avatar, mesma corrente: clipe 1 da imagem, clipes 2 a 8
do último frame do anterior.

### Bloco fixo — **mudou**

Os dois vídeos de referência não são "agitados". O apresentador é **firme e
articulado**, não acelerado: ele segura o olhar, gesticula o tempo todo com as
mãos abertas perto do peito, e marca a palavra importante com uma pausa curta
antes dela — não com volume. Ganha em clareza, não em velocidade.

Troque o bloco de entrega por este:

```
Entrega: tom firme, articulado e direto, como quem explica uma coisa
importante para um amigo e quer ser entendido. Olha direto na lente o
tempo todo, sem desviar. Gesticula com as duas mãos abertas perto do
peito, de forma contínua e natural. Leve inclinação do corpo para a
frente. Marca a palavra importante com uma pausa curta antes dela, não
levantando a voz. Português brasileiro coloquial, claro, sem pressa e
sem arrastar.

Câmera fixa, sem movimento, sem zoom, sem corte, sem transição.
Sem legenda, sem texto na tela, sem letreiro, sem marca d'água.
Sem música, sem trilha, sem efeito sonoro — só a voz dele.
Sem mudar roupa, relógio, cenário ou iluminação.
```

### Montagem de cada clipe

```
Continuação direta da cena anterior, sem corte. A mesma pessoa, na mesma
mesa, com a mesma roupa, o mesmo relógio, a mesma luz e o mesmo fundo,
partindo exatamente da posição em que o frame anterior terminou.

<GESTO DO ROTEIRO>

Ele diz, exatamente estas palavras: "<FALA DO ROTEIRO>"

<BLOCO FIXO>
```

No clipe 1 troque a primeira linha por: `A pessoa da imagem começa com as mãos
entrelaçadas na altura do queixo e as abre ao falar.`

---

## Checklist por clipe

- [ ] a fala saiu exatamente como no roteiro
- [ ] coube nos 10 s sem cortar frase
- [ ] sem legenda e sem música
- [ ] câmera parada
- [ ] suéter, relógio e fundo iguais
- [ ] **frame final limpo**: boca fechada ou quase, olhos abertos

O clipe 3 tem 26 palavras, o mais apertado do lote. Se cortar, use:
*"E a primeira coisa que ele faz é ir atrás do irmão. Achamos o Cristo, ele diz,
e leva o Pedro."*

---

## Depois de gerar

`01.mp4` a `08.mp4`, **separados**, numa pasta só. Me manda que eu monto.
