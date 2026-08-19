#!/usr/bin/env bash
# =============================================================================
# TCJJ Centro — instalador automático para CloudPanel (site estático)
#
# Uso (como root, no terminal do servidor):
#   curl -fsSL https://raw.githubusercontent.com/freezeshake-afk/freezeshake-afk.github.io/main/deploy/install-tcjj.sh | sudo bash
#
# O que faz:
#   1) cria um site estático no CloudPanel para o domínio (se ainda não existir)
#   2) baixa os arquivos do app e publica na raiz do site
#   3) emite o certificado SSL (Let's Encrypt)  -> precisa do DNS já apontando
#
# É seguro rodar de novo (idempotente): atualiza os arquivos e tenta o SSL.
# Variáveis opcionais: TCJJ_DOMAIN (padrão tcjj.com.br), TCJJ_SITEUSER (padrão tcjj)
# =============================================================================
set -uo pipefail

DOMAIN="${TCJJ_DOMAIN:-tcjj.com.br}"
SITEUSER="${TCJJ_SITEUSER:-tcjj}"
RAW="https://raw.githubusercontent.com/freezeshake-afk/freezeshake-afk.github.io/main"
FILES=(index.html qrcode.js manifest.json service-worker.js icon-180.png icon-192.png icon-512.png icon-maskable-512.png)
DOCROOT="/home/${SITEUSER}/htdocs/${DOMAIN}"

echo "======================================================"
echo "  TCJJ Centro — deploy em ${DOMAIN}"
echo "======================================================"

if [ "$(id -u)" -ne 0 ]; then echo "ERRO: rode como root (use sudo)."; exit 1; fi
command -v curl >/dev/null 2>&1 || { echo "ERRO: 'curl' não encontrado."; exit 1; }

# ---- 1) criar o site estático no CloudPanel (se não existir) ----
if [ ! -d "$DOCROOT" ]; then
  if command -v clpctl >/dev/null 2>&1; then
    echo "==> Criando site estático no CloudPanel para ${DOMAIN} ..."
    PASS="Tcjj$(openssl rand -hex 5)A9!"
    if clpctl site:add:static --domainName="$DOMAIN" --siteUser="$SITEUSER" --siteUserPassword="$PASS"; then
      echo "    Site criado. Usuário SFTP: ${SITEUSER}  |  Senha: ${PASS}"
      echo "    (Anote essa senha — serve para acessar os arquivos por SFTP depois.)"
    else
      echo "    AVISO: não consegui criar via clpctl (versões variam)."
      echo "    Crie o site estático '${DOMAIN}' pela interface do CloudPanel"
      echo "    (Sites > + Adicionar Site > Criar um Site Estático, usuário: ${SITEUSER})"
      echo "    e rode este comando de novo."
    fi
  else
    echo "ERRO: 'clpctl' não encontrado. Crie o site estático '${DOMAIN}' pela"
    echo "interface do CloudPanel (usuário do site: ${SITEUSER}) e rode de novo."
  fi
fi

if [ ! -d "$DOCROOT" ]; then
  echo "ERRO: a pasta do site não existe (${DOCROOT})."
  echo "Crie o site no CloudPanel e rode este comando novamente."
  exit 1
fi

# ---- 2) baixar e publicar os arquivos do app ----
echo "==> Baixando o app e publicando em ${DOCROOT} ..."
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
ok=1
for f in "${FILES[@]}"; do
  curl -fsSL "${RAW}/${f}" -o "${TMP}/${f}" || { echo "    falha ao baixar ${f}"; ok=0; }
done
mkdir -p "${TMP}/vendor"
curl -fsSL "${RAW}/vendor/firebase.js" -o "${TMP}/vendor/firebase.js" || { echo "    falha ao baixar vendor/firebase.js"; ok=0; }
[ "$ok" -eq 1 ] || { echo "ERRO: download incompleto. Tente de novo."; exit 1; }

rm -f "${DOCROOT}/index.html"                       # remove o index de exemplo
cp "${TMP}"/*.png "${DOCROOT}/"
cp "${TMP}/index.html" "${TMP}/qrcode.js" "${TMP}/manifest.json" "${TMP}/service-worker.js" "${DOCROOT}/"
mkdir -p "${DOCROOT}/vendor"; cp "${TMP}/vendor/firebase.js" "${DOCROOT}/vendor/"
chown -R "${SITEUSER}:${SITEUSER}" "${DOCROOT}" 2>/dev/null || true
echo "    Arquivos publicados."

# ---- 3) SSL (Let's Encrypt) ----
if command -v clpctl >/dev/null 2>&1; then
  echo "==> Emitindo certificado SSL (Let's Encrypt) ..."
  if clpctl lets-encrypt:install:certificate --domainName="$DOMAIN"; then
    echo "    HTTPS ativo."
  else
    echo "    AVISO: SSL não emitido. Verifique se o DNS de ${DOMAIN} já aponta"
    echo "    para ESTE servidor e rode este comando de novo (ou emita pela interface)."
  fi
fi

echo "======================================================"
echo "  Pronto! Teste em:  https://${DOMAIN}"
echo "  (Se o SSL falhou, ajuste o DNS e rode o comando de novo.)"
echo "======================================================"
