# 🚀 Guia de Atualização na VPS

## Passo a Passo para Atualizar o Content Orchestrator

### 1️⃣ Entrar no diretório do projeto

```bash
cd ~/content-orchestrator
```

### 2️⃣ Atualizar código do GitHub

```bash
git pull origin main
```

### 3️⃣ Verificar se requirements.txt está atualizado

```bash
cat requirements.txt
```

Deve conter:
```
fastapi>=0.100.0
uvicorn
python-dotenv
pydantic>=2.0
pydantic-settings
httpx
playwright>=1.40.0
tenacity
requests
yt-dlp>=2023.12.30
pytubefix>=6.0.0
```

### 4️⃣ Rebuild do container Docker

```bash
cd ~
docker-compose build content-orchestrator
```

### 5️⃣ Reiniciar o container

```bash
docker-compose up -d content-orchestrator
```

### 6️⃣ Verificar logs

```bash
docker-compose logs -f content-orchestrator
```

### 7️⃣ Testar o download (dentro do container)

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
        print('SUCCESS! Arquivo:', result.get('path'))
    else:
        print('ERROR:', result.get('error'))

asyncio.run(test())
"
```

### 8️⃣ Verificar se o arquivo foi baixado

```bash
docker exec -it content-orchestrator ls -lh /app/downloads/teste/@shortspodcuts/
```

## ⚡ Comandos Rápidos (Copiar e Colar)

```bash
# Atualizar código
cd ~/content-orchestrator && git pull origin main && cd ~

# Rebuild e reiniciar
docker-compose build content-orchestrator && docker-compose up -d content-orchestrator

# Ver logs
docker-compose logs -f content-orchestrator
```

## 🔍 Verificar Status

```bash
# Status do container
docker ps | grep content-orchestrator

# Logs recentes
docker-compose logs --tail=50 content-orchestrator

# Entrar no container
docker exec -it content-orchestrator bash
```

## ✅ Verificação Final

Após atualizar, verifique:

1. ✅ Container rodando: `docker ps | grep content-orchestrator`
2. ✅ Requirements atualizado: `docker exec content-orchestrator cat /app/requirements.txt | grep yt-dlp`
3. ✅ Teste de download funcionando

## 🐛 Troubleshooting

### Se o container não iniciar:

```bash
# Ver logs de erro
docker-compose logs content-orchestrator

# Rebuild forçado
docker-compose build --no-cache content-orchestrator
docker-compose up -d content-orchestrator
```

### Se o download falhar:

```bash
# Verificar se yt-dlp está instalado
docker exec content-orchestrator pip list | grep yt-dlp

# Verificar se pytubefix está instalado
docker exec content-orchestrator pip list | grep pytubefix

# Reinstalar dependências
docker exec content-orchestrator pip install --upgrade yt-dlp pytubefix
```
