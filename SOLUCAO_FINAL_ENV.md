# 🔧 Solução Final: Variáveis do Supabase no Container

## ❌ Problema

O `.env` no host está correto, mas o container ainda recebe variáveis do Supabase. Isso significa que elas estão vindo de outro lugar.

## 🔍 Verificar Onde Estão as Variáveis

Execute na VPS:

```bash
# 1. Verificar docker-compose.yml principal
cd /root
cat docker-compose.yml | grep -A 30 content-orchestrator
```

Procure por:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `DATABASE_URL`
- `environment:` (seção que pode ter essas variáveis)

## ✅ Solução 1: Remover do docker-compose.yml Principal

Se encontrar essas variáveis no `docker-compose.yml` principal:

```bash
cd /root
nano docker-compose.yml
```

**Remova ou comente as linhas:**
```yaml
# SUPABASE_URL=...
# SUPABASE_KEY=...
# DATABASE_URL=...
```

**OU se estiverem na seção `environment:` do serviço `content-orchestrator`, remova:**
```yaml
environment:
  # SUPABASE_URL=...  # REMOVER
  # SUPABASE_KEY=...  # REMOVER
  # DATABASE_URL=...  # REMOVER
  STORAGE_TYPE=local
  LOCAL_STORAGE_PATH=/app/downloads
```

Salvar: `Ctrl+X`, depois `Y`, depois `Enter`

```bash
# Reiniciar
docker compose restart content-orchestrator
```

## ✅ Solução 2: Verificar Variáveis de Ambiente do Sistema

As variáveis podem estar definidas no sistema:

```bash
# Verificar se estão definidas
env | grep -i supabase
env | grep -i database
```

Se aparecerem, remova do `/root/.bashrc` ou `/root/.profile`:

```bash
nano ~/.bashrc
# Remover linhas com SUPABASE_URL, SUPABASE_KEY, DATABASE_URL
```

## ✅ Solução 3: Forçar .env Correto no Container

Garantir que o container use o `.env` correto:

```bash
cd /root
docker compose stop content-orchestrator
docker compose rm -f content-orchestrator

# Reconstruir e iniciar
docker compose build content-orchestrator
docker compose up -d content-orchestrator
```

## ✅ Solução 4: Verificar se .env está sendo montado corretamente

Verificar se o `docker-compose.yml` está usando o `.env` correto:

```bash
cd /root
cat docker-compose.yml | grep -A 5 content-orchestrator | grep env_file
```

Deve mostrar:
```yaml
env_file: ./content-orchestrator/.env
```

Se não estiver, adicione ou corrija.

## 🚀 Comando Completo de Verificação e Correção

```bash
# 1. Verificar docker-compose.yml
cd /root
echo "=== Verificando docker-compose.yml ==="
grep -A 30 "content-orchestrator:" docker-compose.yml | grep -E "(SUPABASE|DATABASE|env_file)"

# 2. Se encontrar, editar
nano docker-compose.yml
# Remover variáveis do Supabase

# 3. Parar e remover container
docker compose stop content-orchestrator
docker compose rm -f content-orchestrator

# 4. Reconstruir
docker compose build content-orchestrator

# 5. Iniciar
docker compose up -d content-orchestrator

# 6. Verificar logs
sleep 5
docker logs --tail 30 content-orchestrator

# 7. Testar
curl http://localhost:8002/v1/n8n/health
```

---

## 📝 Checklist

- [ ] `.env` no host está correto (sem Supabase) ✅
- [ ] `docker-compose.yml` principal não tem variáveis do Supabase
- [ ] Variáveis não estão no sistema (`env | grep SUPABASE`)
- [ ] Container reconstruído após mudanças
- [ ] Logs não mostram erros de ValidationError
- [ ] Health check funciona

---

**Execute o comando de verificação primeiro para identificar onde estão as variáveis!**


