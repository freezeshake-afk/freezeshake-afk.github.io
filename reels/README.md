# Fábrica de Reels — Editor de vídeos em lote

Ferramenta web (mobile-first) para editar **vários reels de uma vez**, direto no
navegador. Nenhum vídeo é enviado para servidor — todo o processamento acontece
no aparelho do usuário usando **FFmpeg compilado para WebAssembly**.

Acesse em: `https://freezeshake-afk.github.io/reels/`

## Funcionalidades (baseadas no fluxo dos prints de referência)

- **Editor em lote** — arraste/selecione vários vídeos (MP4, MOV, WebM).
- **Preview 9:16** com linhas tracejadas mostrando onde as bordas serão cortadas.
- **Ajuste fino**: Zoom, Posição vertical e Posição horizontal.
- **Bordas**: cobre/remove a borda superior e inferior (marca d'água, legenda,
  logo) com cor à escolha; modo Manual/Automático + "Detectar automaticamente".
- **Título** (topo) e **Inferior** (rodapé): texto com cor, tamanho e fundo.
- **Overlay**: texto central (marca) e escurecimento do fundo.
- **Modo anti duplicidade** (PLUS/PREMIUM): leve mudança de velocidade (1.02x) e
  espelhamento, para reduzir detecção de conteúdo repetido.
- **Config. em lote** (aplica a todos) ou **Só este vídeo** (ajuste individual).
- **Processar** e baixar cada vídeo pronto (1080×1920, H.264 + AAC).
- Contador do plano grátis, tema claro/escuro.

## Como funciona por dentro

- `index.html` — app completo (UI + lógica + preview em `<canvas>` + exportação).
- `vendor/ffmpeg/` — wrapper leve do `@ffmpeg/ffmpeg` servido **localmente**
  (same-origin) para o Worker interno funcionar sem violar a política de mesma
  origem. O core do FFmpeg (grande) é carregado do CDN sob demanda.
- Usa o core **single-thread** do FFmpeg: dispensa `SharedArrayBuffer` /
  cabeçalhos COOP-COEP e funciona no GitHub Pages e no Safari do iPhone.

### Observações
- Emojis não são gravados no texto do vídeo (limitação do `drawtext`); o texto
  em si funciona normalmente, inclusive com acentos.
- O core do FFmpeg (~32 MB) é baixado na primeira vez que você processa um vídeo.

## Próximas fases (para virar SaaS de verdade)
- Contas de usuário, planos e cobrança (ex.: Stripe/Mercado Pago).
- **Turbo**: processamento em servidor (fila) para entregar em ~30s.
- Painel de uso e limites reais por plano.
