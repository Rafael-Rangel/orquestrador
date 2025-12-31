# 🔧 Correção Rápida: Remover Supabase do .env

## ❌ Problema

O erro mostra que o `.env` ainda tem variáveis do Supabase:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `DATABASE_URL`

Mas o código novo não aceita essas variáveis!

## ✅ Solução Rápida

Execute na VPS:

```bash
# 1. Editar .env
cd /root/content-orchestrator
nano .env
```

**Remova estas 3 linhas:**
```
SUPABASE_URL=...
SUPABASE_KEY=...
DATABASE_URL=...
```

**Deixe apenas:**
```env
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=/app/downloads
PROJECT_NAME=Content Orchestrator
API_V1_STR=/v1
DOMAIN_NAME=postagensapp.shop
ORCHESTRATOR_SUBDOMAIN=orchestrator
SSL_EMAIL=seu-email@exemplo.com
```

**Salvar:** `Ctrl+X`, depois `Y`, depois `Enter`

```bash
# 2. Reiniciar container
cd /root
docker compose restart content-orchestrator

# 3. Verificar logs
docker logs -f content-orchestrator
```

**Deve aparecer:** "Application startup complete" sem erros!

```bash
# 4. Testar
curl http://localhost:8002/v1/n8n/health
```

**Resposta esperada:**
```json
{"status":"ok","message":"n8n integration ready"}
```

---

## 🚀 Comando Rápido (Uma Linha)

Se preferir, pode fazer tudo de uma vez:

```bash
cd /root/content-orchestrator && \
sed -i '/^SUPABASE_URL=/d; /^SUPABASE_KEY=/d; /^DATABASE_URL=/d' .env && \
cd /root && docker compose restart content-orchestrator && \
sleep 3 && curl http://localhost:8002/v1/n8n/health
```

---

## ✅ Verificar se Funcionou

```bash
# Ver conteúdo do .env (não deve ter Supabase)
cat /root/content-orchestrator/.env | grep -i supabase
# (Não deve retornar nada)

# Ver logs
docker logs content-orchestrator | tail -20
# (Não deve ter erros de ValidationError)

# Testar API
curl http://localhost:8002/v1/n8n/health
# (Deve retornar {"status":"ok"...})
```

---

**Pronto!** Depois disso o container deve iniciar normalmente! 🎉


