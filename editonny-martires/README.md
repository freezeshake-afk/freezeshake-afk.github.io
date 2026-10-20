# Pacote de cenas: mártires cristãos

Seis cenas animadas para o [editonny](https://github.com/soumatheusgomes/editonny),
feitas para o nicho de mártires cristãos. O catálogo que vem no editonny é ótimo,
mas é de faturamento, imóveis, saúde, jurídico e criadores — não tem nada de
história da igreja. Estas cenas preenchem esse buraco.

Todas passam no `lint` e no `check` do próprio motor do editonny, e foram
renderizadas de verdade no HyperFrames antes de entrar aqui.

![as seis cenas](preview/contato.png)

---

## Instalar

Primeiro o editonny, se ainda não tiver:

```
git clone https://github.com/soumatheusgomes/editonny
cd editonny && python3 install.py --target both
```

Depois o pacote:

```
cd editonny-martires
python3 instalar.py
```

Ele copia as cenas para `visuals/scenes/` e mescla as entradas em
`visuals/catalog.json`, guardando uma cópia do catálogo original.

> **Toda vez que atualizar o editonny, rode `python3 instalar.py` de novo.**
> A atualização substitui a pasta inteira do pacote e leva junto as cenas de fora.

Conferir: `python3 instalar.py --conferir` — ou `doctor`, que deve dizer
**151 scenes; 0 missing files**.

Sair: `python3 instalar.py --remover`.

---

## As cenas

Todas são `layout: frame` — o painel ocupa a parte de cima e você aparece na
moldura embaixo, igual ao vídeo que serviu de referência.

| cena | quando usar | dura |
|---|---|---|
| `martir-ficha` | abrir a história: nome, anos, cidade e uma linha de contexto | 6,0s |
| `martir-local` | nomear o lugar: a cidade pulsa num campo de mapa, com a província e o ano | 6,0s |
| `martir-linha-tempo` | situar entre as perseguições: um marcador corre a linha e para no imperador escolhido | 7,0s |
| `martir-escolha` | a saída que ofereceram: duas opções, uma é riscada e a outra acende | 6,5s |
| `martir-contador` | quando um número carrega o peso: anos de serviço, idade, quantos morreram | 5,0s |
| `martir-ultimas-palavras` | o pico emocional: a fala do mártir surge linha a linha, com a fonte embaixo | 6,5s |

### Como pedir

Converse normalmente com o editonny — ele lê o catálogo e acha as cenas pelo
`whenToUse`. Se quiser cravar:

```
/editonny
Edita esse vídeo sobre Policarpo. Usa a cena martir-ficha na abertura,
martir-ultimas-palavras quando eu cito a frase dele, e martir-contador
no "oitenta e seis anos".
```

### Parâmetros

Cada cena é editável — é isso que faz uma cena servir para qualquer mártir, não
só para o Policarpo. Os valores ficam no bloco `var P` do HTML da cena copiada
dentro do projeto, e estão descritos em `catalog.martires.json`.

```js
// martir-ultimas-palavras
var P = {
  citacao: "Oitenta e seis anos eu o sirvo|e ele nunca me fez mal algum.|...",
  autor: "Policarpo de Esmirna, 155 d.C.",
  fonte: "Martirio de Policarpo, 9.3",
};
```

O `|` separa linhas (na citação) ou itens (nos marcos da linha do tempo).
Campo vazio esconde o elemento em vez de deixar um buraco.

---

## Mexer no visual

Não edite os HTML em `scenes/` na mão — eles são **gerados**. O arquivo que vale
é o `construir.py`, que guarda o CSS, o HTML e a timeline GSAP de cada cena num
esqueleto comum.

```
# edita construir.py
python3 construir.py     # regera scenes/ e catalog.martires.json
python3 instalar.py      # manda para o editonny
python3 validar.py       # renderiza e confere no motor real
```

O `validar.py` monta um projeto sintético, aplica as seis cenas em sequência,
roda `lint` e `check` do HyperFrames e salva um frame de cada em `preview/`.
Com `--render` ele também gera o mp4 inteiro.

### Duas regras que não dá para quebrar

Aprendi as duas na marra, com o `check` do motor reprovando:

1. **Nada de criar elemento ou montar nome de classe no JavaScript.** O
   `apply.py` do editonny renomeia os identificadores para cada cópia da cena ser
   independente. Ele renomeia IDs literais no HTML, no CSS e no JS — mas uma
   string como `className = "t-marco" + (...)` ele trata como prefixo de ID
   dinâmico: reescreve a string no JS e **não** o `.t-marco` do CSS. A classe
   deixa de casar e a cena desmonta. Por isso tudo aqui é estático: os elementos
   existem no HTML, com IDs literais, e o JS só preenche texto e posição.
2. **Nada de `scale` nas animações.** O renderizador não aceita; o helper `lim()`
   converte `scaleX`/`scaleY` em `clip-path`. Use opacidade, `x`/`y`, `rotation`
   e `clipPath`.

O `check` também cobra sobreposição de texto, contraste WCAG AA e oclusão. Quando
a sobreposição for de propósito — o risco vermelho por cima do texto na
`martir-escolha` — marque com `data-layout-allow-occlusion`.

---

## Área útil

O painel vive em 1080×992, com o conteúdo importante entre x 140–940 e
y 230–850. Abaixo disso entra a moldura do apresentador. O `validar.py` usa a
caixa padrão do editonny:

```json
{"frame": {"box": [36, 912, 1008, 990]}}
```

O vídeo de referência usa uma moldura bem menor (medi 585×488 numa tela de
1080×1920, começando em x 248, y 1020). Se quiser aquele enquadramento mais
apertado, é esse o valor da caixa.

---

## Cuidado com o conteúdo

As datas, números e citações que vêm como padrão são **do Policarpo de Esmirna**,
e servem de exemplo. Troque pelos dados do mártir de cada vídeo e confira a
fonte antes de publicar — o `whenToUse` de cada cena fala em ilustrar o que foi
dito, não em inventar número nem atribuir frase a quem não disse.

Fontes primárias que costumam resolver: *Martírio de Policarpo*, a
*História Eclesiástica* de Eusébio, as cartas de Inácio de Antioquia, a
*Paixão de Perpétua e Felicidade* e a carta de Plínio a Trajano.

---

## Licença

As cenas deste pacote são MIT, igual ao editonny. O editonny é de
Matheus Gomes; este pacote não é oficial e não é mantido por ele.
