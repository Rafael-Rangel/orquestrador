# 🚀 Guia de Deploy - Content Orchestrator

Este guia explica como fazer deploy do Content Orchestrator na sua VPS, com duas opções: **via GitHub** (recomendado) ou **manual**.

---

## 📋 Pré-requisitos

- VPS com Docker e Docker Compose instalados
- Acesso SSH à VPS
- Conta no GitHub (opcional, para método 1)
- Credenciais do Supabase configuradas

---

## 🎯 Opção 1: Deploy via GitHub (Recomendado)

### Vantagens
- ✅ Fácil de atualizar (git pull)
- ✅ Versionamento do código
- ✅ Backup automático
- ✅ Colaboração facilitada
- ✅ Histórico de mudanças

### Passo 1: Preparar o Repositório Local

#### 1.1. Criar arquivo `.gitignore`

Crie um arquivo `.gitignore` na raiz do projeto:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Ambiente
.env
.env.local
.env.*.local

# Downloads e Logs
downloads/
logs/
data/
*.log

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore
```

#### 1.2. Criar arquivo `.env.example`

Crie um arquivo `.env.example` com as variáveis necessárias (sem valores sensíveis):

```env
# Supabase / Database
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-supabase
DATABASE_URL=postgresql+asyncpg://postgres:senha@db.seu-projeto.supabase.co:5432/postgres

# Storage
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=/app/downloads

# Traefik (para deploy)
DOMAIN_NAME=postagensapp.shop
ORCHESTRATOR_SUBDOMAIN=orchestrator
SSL_EMAIL=seu-email@exemplo.com
```

#### 1.3. Inicializar Git e Fazer Push

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Commit inicial
git commit -m "Initial commit: Content Orchestrator"

# Criar repositório no GitHub (via web ou CLI)
# Depois adicionar remote:
git remote add origin https://github.com/seu-usuario/content-orchestrator.git

# Fazer push
git branch -M main
git push -u origin main
```

### Passo 2: Deploy na VPS

#### 2.1. Conectar na VPS

```bash
ssh root@seu-ip-vps
```

#### 2.2. Clonar o Repositório

```bash
cd /root
git clone https://github.com/seu-usuario/content-orchestrator.git
cd content-orchestrator
```

#### 2.3. Criar Arquivo `.env`

```bash
# Copiar exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

**Conteúdo do `.env`:**

```env
SUPABASE_URL=https://tvloytursdkrwnfzwbtp.supabase.co
SUPABASE_KEY=sb_secret_8ludQHaAn4delkAPLfkGpg_KPZCc3-k
DATABASE_URL=postgresql+asyncpg://postgres:Rr%400924660102@db.tvloytursdkrwnfzwbtp.supabase.co:5432/postgres

STORAGE_TYPE=local
LOCAL_STORAGE_PATH=/app/downloads

DOMAIN_NAME=postagensapp.shop
ORCHESTRATOR_SUBDOMAIN=orchestrator
SSL_EMAIL=stackflow.soft@gmail.com
```

**Importante:** Na `DATABASE_URL`, substitua `@` por `%40` na senha.

#### 2.4. Adicionar ao Docker Compose Principal

Se você já tem um `docker-compose.yml` na raiz da VPS, adicione o serviço:

```bash
cd /root
nano docker-compose.yml
```

Adicione o serviço `content-orchestrator`:

```yaml
services:
  # ... seus outros serviços ...
  
  content-orchestrator:
    build:
      context: ./content-orchestrator
      dockerfile: Dockerfile
    container_name: content-orchestrator
    restart: always
    env_file: ./content-orchestrator/.env
    environment:
      - STORAGE_TYPE=local
      - LOCAL_STORAGE_PATH=/app/downloads
    volumes:
      - ./content-orchestrator/downloads:/app/downloads
      - ./content-orchestrator/logs:/app/logs
      - ./content-orchestrator/data:/app/data
    ports:
      - "127.0.0.1:8002:8000"
    labels:
      - traefik.enable=true
      - traefik.http.routers.content-orchestrator.rule=Host(`orchestrator.${DOMAIN_NAME}`)
      - traefik.http.routers.content-orchestrator.entrypoints=web,websecure
      - traefik.http.routers.content-orchestrator.tls=true
      - traefik.http.routers.content-orchestrator.tls.certresolver=mytlschallenge
      - traefik.http.services.content-orchestrator.loadbalancer.server.port=8000
    command: "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    networks:
      - default
```

#### 2.5. Construir e Iniciar

```bash
# Voltar para raiz
cd /root

# Construir imagem
docker compose build content-orchestrator

# Iniciar serviço
docker compose up -d content-orchestrator

# Verificar logs
docker logs -f content-orchestrator
```

#### 2.6. Verificar Deploy

```bash
# Health check
curl http://localhost:8002/health

# Deve retornar:
# {"status":"healthy","database":"connected"}
```

### Passo 3: Atualizações Futuras

Para atualizar o código na VPS:

```bash
# Conectar na VPS
ssh root@seu-ip-vps

# Ir para o diretório do projeto
cd /root/content-orchestrator

# Atualizar código
git pull origin main

# Reconstruir e reiniciar
cd /root
docker compose build content-orchestrator
docker compose up -d content-orchestrator

# Verificar
docker logs -f content-orchestrator
```

---

## 🛠️ Opção 2: Deploy Manual

### Quando Usar
- Não quer usar GitHub
- Deploy único sem atualizações frequentes
- Ambiente restrito sem acesso a Git

### Passo 1: Preparar Arquivos Localmente

#### 1.1. Compactar o Projeto

**No Windows (PowerShell):**

```powershell
# Instalar 7-Zip ou usar WSL
# Com 7-Zip:
7z a -tgzip content-orchestrator.tar.gz . -xr!.git -xr!__pycache__ -xr!*.pyc -xr!.env -xr!downloads -xr!logs -xr!data
```

**No Linux/Mac:**

```bash
tar -czf content-orchestrator.tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.env' \
  --exclude='downloads' \
  --exclude='logs' \
  --exclude='data' \
  .
```

### Passo 2: Enviar para VPS

#### 2.1. Via SCP

```bash
# Do seu computador
scp content-orchestrator.tar.gz root@seu-ip-vps:/root/
```

#### 2.2. Via SFTP (FileZilla, WinSCP, etc.)

- Conecte na VPS via SFTP
- Envie o arquivo `content-orchestrator.tar.gz` para `/root/`

### Passo 3: Extrair e Configurar na VPS

```bash
# Conectar na VPS
ssh root@seu-ip-vps

# Extrair arquivo
cd /root
tar -xzf content-orchestrator.tar.gz -C content-orchestrator
cd content-orchestrator

# Criar .env
nano .env
# (Cole o conteúdo do .env com suas credenciais)

# Criar diretórios
mkdir -p downloads logs data
```

### Passo 4: Adicionar ao Docker Compose

Siga os mesmos passos da **Opção 1, Passo 2.4**.

### Passo 5: Construir e Iniciar

Siga os mesmos passos da **Opção 1, Passo 2.5**.

---

## 🔧 Script de Deploy Automatizado

Crie um script para facilitar atualizações:

### `deploy.sh` (na VPS)

```bash
#!/bin/bash
set -e

echo "🚀 Iniciando deploy do Content Orchestrator..."

# Ir para diretório do projeto
cd /root/content-orchestrator

# Atualizar código (se usando Git)
if [ -d .git ]; then
    echo "📥 Atualizando código do GitHub..."
    git pull origin main
else
    echo "⚠️  Repositório Git não encontrado. Pulando atualização."
fi

# Voltar para raiz
cd /root

# Construir imagem
echo "🔨 Construindo imagem Docker..."
docker compose build content-orchestrator

# Parar serviço antigo
echo "🛑 Parando serviço antigo..."
docker compose stop content-orchestrator || true

# Iniciar novo serviço
echo "▶️  Iniciando novo serviço..."
docker compose up -d content-orchestrator

# Aguardar inicialização
echo "⏳ Aguardando inicialização..."
sleep 5

# Verificar saúde
echo "🏥 Verificando saúde do serviço..."
if curl -s http://localhost:8002/health > /dev/null; then
    echo "✅ Deploy concluído com sucesso!"
    echo "📊 Status:"
    docker ps | grep content-orchestrator
else
    echo "❌ Erro: Serviço não está respondendo"
    echo "📋 Logs:"
    docker logs --tail 50 content-orchestrator
    exit 1
fi
```

**Tornar executável:**

```bash
chmod +x /root/content-orchestrator/deploy.sh
```

**Usar:**

```bash
/root/content-orchestrator/deploy.sh
```

---

## 🔐 Segurança

### 1. Proteger Credenciais

**Nunca commite o arquivo `.env` no Git!**

```bash
# Verificar se .env está no .gitignore
cat .gitignore | grep .env

# Se não estiver, adicione:
echo ".env" >> .gitignore
```

### 2. Restringir Acesso à API

**Recomendado:** Adicionar autenticação básica ou API Key:

```python
# app/api/dependencies.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key
```

### 3. Firewall

Na VPS, certifique-se de que apenas as portas necessárias estão abertas:

```bash
# Verificar portas abertas
ufw status

# Permitir apenas SSH e portas do Traefik
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

---

## 📊 Verificação Pós-Deploy

### Checklist

- [ ] Container está rodando: `docker ps | grep content-orchestrator`
- [ ] Health check OK: `curl http://localhost:8002/health`
- [ ] Documentação acessível: `curl http://localhost:8002/docs`
- [ ] Banco de dados conectado (verificar logs)
- [ ] Traefik roteando corretamente (se usando)
- [ ] SSL funcionando (se usando Traefik)

### Comandos Úteis

```bash
# Ver logs em tempo real
docker logs -f content-orchestrator

# Ver status do container
docker ps | grep content-orchestrator

# Ver uso de recursos
docker stats content-orchestrator

# Reiniciar serviço
docker compose restart content-orchestrator

# Parar serviço
docker compose stop content-orchestrator

# Remover serviço (cuidado!)
docker compose down content-orchestrator
```

---

## 🐛 Troubleshooting

### Problema: Container não inicia

```bash
# Ver logs detalhados
docker logs content-orchestrator

# Verificar se .env existe
ls -la /root/content-orchestrator/.env

# Verificar variáveis
docker compose config
```

### Problema: Erro de conexão com banco

```bash
# Testar conexão manualmente
docker exec -it content-orchestrator python -c "
from app.core.database import engine
import asyncio
async def test():
    async with engine.begin() as conn:
        print('✅ Conexão OK')
asyncio.run(test())
"
```

### Problema: Porta já em uso

```bash
# Verificar qual processo está usando a porta
lsof -i :8002

# Ou mudar a porta no docker-compose.yml
ports:
  - "127.0.0.1:8003:8000"  # Mude 8002 para 8003
```

---

## 📝 Próximos Passos

Após o deploy bem-sucedido:

1. **Configurar n8n:**
   - Adicionar workflow de processamento
   - Configurar cron schedule
   - Testar endpoints

2. **Criar Grupos e Fontes:**
   ```bash
   curl -X POST http://localhost:8002/v1/groups \
     -H "Content-Type: application/json" \
     -d '{"name": "Culinária", "status": "active"}'
   ```

3. **Monitorar:**
   - Configurar alertas no n8n
   - Monitorar logs regularmente
   - Verificar espaço em disco

---

## ✅ Resumo

**Método Recomendado (GitHub):**
1. Push código para GitHub
2. Clone na VPS
3. Configure `.env`
4. Adicione ao `docker-compose.yml`
5. `docker compose up -d`

**Método Manual:**
1. Compacte projeto
2. Envie para VPS via SCP
3. Extraia e configure
4. Adicione ao `docker-compose.yml`
5. `docker compose up -d`

**Atualizações:**
- GitHub: `git pull` + `docker compose build && up`
- Manual: Reenvie arquivos e reconstrua

---

**Boa sorte com o deploy! 🚀**

