# 🔍 Diagnóstico: Por que funciona localmente mas não na VPS?

## Possíveis causas:

### 1. **IP da VPS bloqueado pelo YouTube**
- O YouTube pode estar bloqueando o IP da VPS mais agressivamente
- **Solução**: Usar cookies válidos (já configurado)

### 2. **Versão do yt-dlp diferente**
- Windows pode ter versão mais nova/antiga
- **Verificar**: `yt-dlp --version` em ambos os ambientes

### 3. **Dependências faltando no Ubuntu**
- Pode faltar alguma biblioteca no Ubuntu
- **Verificar**: ffmpeg, Python, bibliotecas Python

### 4. **Problemas de rede/firewall**
- Firewall bloqueando conexões
- Proxy ou configurações de rede diferentes

### 5. **Cookies inválidos/expirados**
- Cookies podem ter expirado
- **Solução**: Exportar novos cookies do navegador

### 6. **Cliente Android não funciona na VPS**
- Pode ser bloqueio específico do IP/região
- **Solução**: Tentar outros clientes ou usar cookies

## Como diagnosticar:

### Na VPS, execute:

```bash
docker exec -it content-orchestrator bash

# Verificar versões
python3 --version
yt-dlp --version
ffmpeg -version

# Testar conectividade
curl -I https://www.youtube.com

# Ver IP da VPS
curl -s ifconfig.me

# Testar download SEM cookies (cliente android)
yt-dlp --extractor-args "youtube:player_client=android" \
  "https://www.youtube.com/watch?v=jNQXAC9IVRw" \
  --skip-download

# Testar download COM cookies (cliente android)
yt-dlp --cookies /app/data/cookies.txt \
  --extractor-args "youtube:player_client=android" \
  "https://www.youtube.com/watch?v=jNQXAC9IVRw" \
  --skip-download
```

## Soluções possíveis:

### Solução 1: Atualizar yt-dlp na VPS
```bash
docker exec -it content-orchestrator pip install --upgrade yt-dlp
```

### Solução 2: Testar sem cookies primeiro
Remova temporariamente o arquivo cookies.txt e teste:
```bash
docker exec -it content-orchestrator mv /app/data/cookies.txt /app/data/cookies.txt.backup
# Testar download
# Se funcionar, o problema são os cookies
```

### Solução 3: Atualizar cookies
- Exporte novos cookies do navegador
- Envie para a VPS novamente

### Solução 4: Usar proxy/VPN
Se o IP estiver bloqueado, pode precisar de proxy (mais complexo)

## Comparação Local vs VPS:

| Item | Local (Windows) | VPS (Ubuntu/Docker) |
|------|----------------|---------------------|
| Sistema | Windows | Ubuntu Linux |
| Python | 3.14.0 | 3.11 (no container) |
| yt-dlp | ? | ? (verificar) |
| Cookies | Não tinha | Tem cookies.txt |
| Cliente usado | android (sem cookies) | Tentando mweb/web (com cookies) |
| Resultado | ✅ Funciona | ❌ Não funciona |

## Próximo passo:

Execute o script de diagnóstico na VPS para identificar a causa exata:

```bash
# Copiar script para container
docker cp diagnostico_vps.sh content-orchestrator:/app/
docker exec -it content-orchestrator bash /app/diagnostico_vps.sh
```

