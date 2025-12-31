# 🎭 Setup do Playwright - Guia Completo

## O que foi implementado:

✅ **Projeto refeito usando Playwright**
- Substitui pytube/yt-dlp por Playwright
- Simula navegador real (Chromium headless)
- Extrai URL direta do vídeo
- Faz download usando httpx
- yt-dlp como fallback automático

## Como funciona:

1. **Playwright abre navegador headless**
2. **Navega até o vídeo do YouTube**
3. **Extrai URL direta do vídeo** (3 métodos diferentes)
4. **Faz download usando httpx**
5. **Se falhar, usa yt-dlp como fallback**

## Atualizar na VPS:

```bash
cd /root/content-orchestrator
git pull origin main
cd /root
docker compose build content-orchestrator
docker compose up -d content-orchestrator
```

⚠️ **O build pode demorar** porque está instalando:
- Playwright
- Chromium browser
- Dependências do sistema

## Testar:

```bash
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
    if result.get('status') == 'completed':
        print('✅ Sucesso! Arquivo:', result.get('path'))
    else:
        print('❌ Erro:', result.get('error'))

asyncio.run(test())
"
```

## Vantagens do Playwright:

✅ **Simula navegador real** - menos bloqueios
✅ **Executa JavaScript** - resolve desafios automaticamente
✅ **Mais confiável** - funciona como navegador normal
✅ **Fallback automático** - se falhar, usa yt-dlp

## Possíveis Problemas:

### 1. Build demora muito
- Normal, está instalando Chromium (~300MB)
- Pode levar 5-10 minutos

### 2. Erro de memória
- Playwright precisa de mais RAM
- Aumentar memória do container se necessário

### 3. Timeout
- Vídeos grandes podem demorar
- Timeout configurado para 60 segundos

## Próximos Passos:

1. ✅ Fazer build na VPS
2. ✅ Testar download
3. ✅ Verificar logs se houver erro

