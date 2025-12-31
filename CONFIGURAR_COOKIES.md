# 🍪 Guia: Configurar Cookies do YouTube para Download

## Por que precisamos de cookies?

O YouTube está bloqueando downloads sem autenticação. Usando cookies do seu navegador, o yt-dlp consegue fazer download como se fosse você navegando normalmente.

---

## 📋 Método 1: Usando Extensão do Navegador (RECOMENDADO - Mais Fácil)

### Passo 1: Instalar Extensão

**Chrome/Edge:**
1. Acesse: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
2. Clique em "Adicionar ao Chrome"

**Firefox:**
1. Acesse: https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/
2. Clique em "Adicionar ao Firefox"

### Passo 2: Exportar Cookies

1. **Abra o YouTube** no navegador: https://www.youtube.com
2. **Faça login** na sua conta do YouTube (se ainda não estiver logado)
3. **Clique no ícone da extensão** na barra de ferramentas
4. Selecione **"youtube.com"**
5. Clique em **"Export"** ou **"Copiar"**
6. **Salve** o conteúdo em um arquivo chamado `cookies.txt`

### Passo 3: Enviar para VPS

**Opção A: Usando SCP (linha de comando)**

No PowerShell do Windows:
```powershell
scp cookies.txt root@srv1011759:/root/content-orchestrator/data/cookies.txt
```

**Opção B: Usando WinSCP (interface gráfica)**

1. Baixe e instale WinSCP: https://winscp.net/
2. Conecte-se à VPS:
   - Host: `srv1011759` (ou IP da VPS)
   - Usuário: `root`
   - Senha: (sua senha)
3. Navegue até `/root/content-orchestrator/data/`
4. Arraste o arquivo `cookies.txt` para lá

**Opção C: Usando FileZilla**

1. Baixe FileZilla: https://filezilla-project.org/
2. Conecte via SFTP:
   - Host: `sftp://srv1011759` (ou IP)
   - Usuário: `root`
   - Senha: (sua senha)
3. Navegue até `/root/content-orchestrator/data/`
4. Faça upload do `cookies.txt`

---

## 📋 Método 2: Usando yt-dlp Localmente

Se você tem yt-dlp instalado localmente:

### Passo 1: Exportar Cookies

No PowerShell:
```powershell
# Exportar cookies do Chrome
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com"

# Ou do Firefox
yt-dlp --cookies-from-browser firefox --cookies cookies.txt "https://www.youtube.com"

# Ou do Edge
yt-dlp --cookies-from-browser edge --cookies cookies.txt "https://www.youtube.com"
```

### Passo 2: Enviar para VPS

Mesmo processo do Método 1, Passo 3.

---

## ✅ Verificar se Funcionou

Na VPS, execute:

```bash
# Verificar se o arquivo existe
ls -la /root/content-orchestrator/data/cookies.txt

# Verificar dentro do container
docker exec -it content-orchestrator ls -la /app/data/cookies.txt

# Testar download manualmente
docker exec -it content-orchestrator bash
cd /app/downloads/teste/@shortspodcuts/
yt-dlp "https://www.youtube.com/shorts/qlIKbXlFkiE" \
  --cookies /app/data/cookies.txt \
  --extractor-args "youtube:player_client=android" \
  -o "qlIKbXlFkiE.%(ext)s"
```

Se funcionar, você verá o download iniciar sem erros!

---

## 🔄 Atualizar Cookies

Os cookies expiram após algum tempo. Quando parar de funcionar:

1. Repita o processo de exportação
2. Envie o novo arquivo para a VPS (substitua o antigo)
3. Reinicie o container (opcional, mas recomendado):
   ```bash
   docker compose restart content-orchestrator
   ```

---

## 🎯 Formato do Arquivo cookies.txt

O arquivo deve ter este formato (exemplo):

```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	FALSE	1735689600	VISITOR_INFO1_LIVE	abc123...
.youtube.com	TRUE	/	FALSE	1735689600	YSC	def456...
```

---

## ⚠️ Importante

- **NÃO compartilhe** seu arquivo `cookies.txt` publicamente
- Ele contém suas credenciais de sessão
- Mantenha-o seguro e privado
- Se suspeitar que foi comprometido, faça logout no YouTube e gere novos cookies

