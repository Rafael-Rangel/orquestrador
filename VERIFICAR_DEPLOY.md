# ✅ Verificação Pós-Deploy

## 🎯 Comandos para Verificar se Está Funcionando

### 1. Verificar se Container Está Rodando

```bash
docker ps | grep content-orchestrator
```

**Deve mostrar:** Container com status "Up"

### 2. Verificar Logs

```bash
docker logs -f content-orchestrator
```

**Procure por:**
- ✅ "Application startup complete"
- ✅ Sem erros de banco de dados
- ✅ Sem erros de conexão Supabase

### 3. Testar Health Check

```bash
# Health check básico
curl http://localhost:8002/health

# Health check n8n
curl http://localhost:8002/v1/n8n/health
```

**Resposta esperada:**
```json
{"status":"ok","message":"n8n integration ready"}
```

### 4. Testar Endpoint de Fetch

```bash
curl -X POST http://localhost:8002/v1/fetch/run \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "youtube",
    "external_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
    "group_name": "teste"
  }'
```

**Resposta esperada:**
```json
{
  "status": "completed",
  "videos_found": X,
  "videos": [...]
}
```

### 5. Verificar .env (Importante!)

```bash
cat /root/content-orchestrator/.env
```

**NÃO deve ter:**
- ❌ SUPABASE_URL
- ❌ SUPABASE_KEY
- ❌ DATABASE_URL

**DEVE ter:**
- ✅ STORAGE_TYPE=local
- ✅ LOCAL_STORAGE_PATH=/app/downloads
- ✅ PROJECT_NAME=Content Orchestrator
- ✅ API_V1_STR=/v1

### 6. Verificar Documentação

```bash
# Acessar via navegador ou curl
curl http://localhost:8002/docs
```

---

## 🐛 Problemas Comuns

### Container não inicia

```bash
# Ver logs detalhados
docker logs content-orchestrator

# Verificar se porta está livre
netstat -tulpn | grep 8002

# Verificar .env
cat /root/content-orchestrator/.env
```

### Erro de dependências

```bash
# Reconstruir do zero
cd /root
docker compose build --no-cache content-orchestrator
docker compose up -d content-orchestrator
```

### Erro de variáveis de ambiente

```bash
# Verificar .env
cat /root/content-orchestrator/.env

# Se faltar, criar:
cd /root/content-orchestrator
nano .env
# (Cole o conteúdo correto - veja ATUALIZAR_VPS.md)
```

---

## ✅ Checklist de Verificação

- [ ] Container está rodando (`docker ps`)
- [ ] Logs sem erros (`docker logs`)
- [ ] Health check responde (`curl /health`)
- [ ] N8N health check responde (`curl /v1/n8n/health`)
- [ ] .env está correto (sem Supabase)
- [ ] Documentação acessível (`/docs`)
- [ ] Endpoint de fetch funciona

---

## 🎉 Se Tudo Está OK

Agora você pode:

1. **Configurar n8n:** Veja `GUIA_N8N_FLUXO.md`
2. **Criar Google Sheets:** Com as 4 abas (Fontes, Vídeos, Destinos, Histórico)
3. **Criar workflows no n8n:** Seguindo o guia

---

## 📝 Próximos Passos

1. ✅ Deploy concluído
2. ⏭️ Configurar Google Sheets
3. ⏭️ Criar workflows no n8n
4. ⏭️ Testar fluxo completo

**Pronto para usar!** 🚀


