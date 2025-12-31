# 🚫 Solução para Bloqueio de IP na VPS

## Problema Identificado

O YouTube está bloqueando o IP da VPS. Tanto `pytube`, `pytubefix` quanto `yt-dlp` estão falhando com:
- `HTTP Error 400: Bad Request`
- `Sign in to confirm you're not a bot`

## ✅ Soluções Disponíveis

### **Solução 1: Download Local + Upload para VPS** ⭐ (RECOMENDADA)

**Como funciona:**
- Script no seu PC faz download (já funciona!)
- Envia automaticamente para VPS
- VPS processa e publica

**Implementação:**

Criar script `download_local.py` no seu PC:

```python
import subprocess
import os
import paramiko

def download_and_upload(url, video_id, vps_host, vps_user, vps_path):
    # Download local
    print(f"Baixando {url}...")
    subprocess.run(['yt-dlp', url, '-o', f'{video_id}.%(ext)s'])
    
    # Encontrar arquivo baixado
    for file in os.listdir('.'):
        if file.startswith(video_id):
            # Upload para VPS
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(vps_host, username=vps_user)
            
            sftp = ssh.open_sftp()
            sftp.put(file, f'{vps_path}/{file}')
            sftp.close()
            ssh.close()
            
            # Limpar
            os.remove(file)
            print(f"✅ Enviado para VPS: {vps_path}/{file}")
            return True
    
    return False
```

---

### **Solução 2: Usar Proxy/VPN na VPS**

**Como funciona:**
- Container Docker com VPN integrada
- Downloads passam por VPN
- Evita bloqueios de IP

**Implementação:**
- Usar imagem Docker com VPN (ex: `dperson/openvpn-client`)
- Ou configurar proxy no código

---

### **Solução 3: API de Terceiros** ⭐⭐

**Serviços disponíveis:**
- **RapidAPI YouTube Downloader**
- **Apify YouTube Scraper**
- **ScraperAPI**

**Vantagens:**
- ✅ Sem bloqueios
- ✅ Mantido por terceiros
- ✅ Escalável

**Desvantagens:**
- ❌ Custo (pode ter limites gratuitos)

---

### **Solução 4: Atualizar pytubefix e Testar**

O `pytubefix` que acabei de adicionar pode funcionar melhor. Teste:

```bash
cd /root/content-orchestrator
git pull origin main
cd /root
docker compose build content-orchestrator
docker compose up -d content-orchestrator

# Testar
docker exec -it content-orchestrator bash
cd /app
python3 -c "
import sys
sys.path.insert(0, '/app')
from app.services.downloader.service import DownloaderService
import asyncio

async def test():
    service = DownloaderService()
    result = await service.download_video(
        video_url='https://www.youtube.com/shorts/qlIKbXlFkiE',
        platform='youtube',
        external_video_id='qlIKbXlFkiE',
        group_name='teste',
        source_name='@ShortsPodcuts'
    )
    print('Status:', result.get('status'))
    print('Resultado:', result)

asyncio.run(test())
"
```

---

## 🎯 Recomendação Final

**Para funcionar AGORA:**
1. ✅ Use **Solução 1** (Download Local + Upload)
   - Funciona 100% (já testado)
   - Sem bloqueios
   - Implementação rápida

**Para produção a longo prazo:**
2. ✅ Use **Solução 3** (API de Terceiros)
   - Mais confiável
   - Sem manutenção
   - Escalável

---

## 📝 Próximos Passos

**Qual solução você prefere implementar?**

1. **Solução 1**: Criar script de download local + upload
2. **Solução 3**: Integrar API de terceiros (RapidAPI, etc)
3. **Testar pytubefix primeiro**: Ver se funciona agora

Me diga qual você prefere e eu implemento!

