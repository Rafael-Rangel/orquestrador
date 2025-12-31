# 🔧 Teste de Solução na VPS

## Diagnóstico do Problema

O yt-dlp está falhando mesmo com:
- ✅ EJS instalado (`npm list -g ejs`)
- ✅ yt-dlp[js] instalado
- ✅ Cookies configurados

## Testes a Fazer na VPS

### Teste 1: Sem Cookies (como funciona localmente)

```bash
docker exec -it content-orchestrator bash

# Mover cookies temporariamente
mv /app/data/cookies.txt /app/data/cookies.txt.backup

# Testar sem cookies
cd /app/downloads/teste/@shortspodcuts/
yt-dlp "https://www.youtube.com/shorts/qlIKbXlFkiE" \
  --extractor-args "youtube:player_client=android" \
  -o "qlIKbXlFkiE.%(ext)s"
```

**Se funcionar**: O problema são os cookies (expirados/inválidos)
**Se não funcionar**: O IP da VPS está bloqueado pelo YouTube

### Teste 2: Verificar se Node.js está sendo detectado

```bash
docker exec -it content-orchestrator bash

# Verificar Node.js
node --version
npm --version

# Verificar se yt-dlp detecta Node.js
yt-dlp --verbose "https://www.youtube.com/watch?v=jNQXAC9IVRw" --skip-download 2>&1 | grep -i "js\|node\|runtime"
```

### Teste 3: Atualizar Cookies

Se o Teste 1 funcionar sem cookies, os cookies estão expirados:

1. Exporte novos cookies do navegador
2. Envie para VPS: `/root/content-orchestrator/data/cookies.txt`
3. Teste novamente

### Teste 4: Tentar Cliente TV (sem cookies)

```bash
yt-dlp "https://www.youtube.com/shorts/qlIKbXlFkiE" \
  --extractor-args "youtube:player_client=tv" \
  -o "qlIKbXlFkiE.%(ext)s"
```

## Soluções Possíveis

### Solução A: Cookies Expirados
- Exportar novos cookies
- Enviar para VPS
- Testar novamente

### Solução B: IP Bloqueado
- Usar proxy/VPN (complexo)
- Tentar outros clientes
- Aguardar desbloqueio do IP

### Solução C: Configurar yt-dlp explicitamente
- Adicionar configuração para usar Node.js
- Verificar variáveis de ambiente

