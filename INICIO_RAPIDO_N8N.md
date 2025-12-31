# 🚀 Início Rápido: Fluxo no n8n

## 📊 Passo 1: Criar Google Sheets

Crie um Google Sheets com estas 4 abas:

### Aba 1: **Fontes**
| platform | external_id | group_name | status | ultima_busca |
|----------|-------------|------------|--------|--------------|
| youtube | UCxxxxx | tecnologia | active | 2024-01-15 |
| instagram | @perfil | tecnologia | active | 2024-01-15 |

### Aba 2: **Vídeos Encontrados**
| video_id | platform | external_id | title | url | duration | view_count | group_name | status | data_encontrado |
|----------|----------|-------------|-------|-----|----------|------------|------------|--------|-----------------|
| abc123 | youtube | UCxxxxx | Vídeo 1 | https://... | 300 | 1000 | tecnologia | discovered | 2024-01-15 |

**Status:** `discovered`, `downloaded`, `published`, `error`

### Aba 3: **Destinos**
| platform | account_id | group_name | daily_limit | status |
|----------|------------|------------|-------------|--------|
| youtube | UCyyyyy | tecnologia | 3 | active |
| instagram | @canal | tecnologia | 5 | active |

### Aba 4: **Histórico de Publicações**
| video_id | destination_platform | destination_account | result | platform_post_id | error_message | published_at |
|----------|----------------------|---------------------|--------|------------------|---------------|--------------|
| abc123 | youtube | UCyyyyy | success | yt_12345 | - | 2024-01-15 10:00 |

---

## 🔄 Fluxo Completo no n8n

### **Workflow 1: Buscar Novos Vídeos** (Executar 1x por dia)

```
1. Google Sheets (Read) → Ler Fontes ativas
2. Code/Set → Formatar JSON para API
3. HTTP Request → POST /v1/n8n/process-sources
   Body: {
     "sources": [
       {"platform": "youtube", "external_id": "UCxxxxx", "group_name": "tecnologia"}
     ]
   }
4. Split → Separar array de vídeos
5. Google Sheets (Read) → Verificar se vídeo já existe
6. IF → Se não existe
7. Google Sheets (Append) → Adicionar novo vídeo (status: discovered)
```

**Trigger:** Cron (diário às 8h) ou Manual

---

### **Workflow 2: Baixar Vídeos** (Executar a cada 30 minutos)

```
1. Google Sheets (Read) → Ler vídeos com status "discovered"
2. Loop → Para cada vídeo
   a. HTTP Request → POST /v1/download
      Body: {
        "video_url": "{{$json.url}}",
        "platform": "{{$json.platform}}",
        "external_video_id": "{{$json.video_id}}",
        "group_name": "{{$json.group_name}}",
        "source_name": "{{$json.external_id}}"
      }
   b. Wait → Aguardar 5-10 minutos
   c. Google Sheets (Update) → Atualizar status para "downloaded"
```

**Trigger:** Cron (a cada 30 minutos)

---

### **Workflow 3: Selecionar e Publicar** (Executar a cada hora)

```
1. Google Sheets (Read) → Ler destinos ativos
2. Loop → Para cada destino
   a. Google Sheets (Read) → Ler vídeos "downloaded" do mesmo grupo
   b. IF → Se tem vídeos disponíveis (não publicados para este destino)
   c. HTTP Request → POST /v1/select
      Body: {
        "destination_platform": "{{destino.platform}}",
        "destination_account_id": "{{destino.account_id}}",
        "group_name": "{{destino.group_name}}",
        "available_videos": [/* vídeos do passo a */]
      }
   d. YouTube/Instagram/TikTok → Publicar vídeo (usar node específico da plataforma)
   e. HTTP Request → POST /v1/confirm_publish
      Body: {
        "video_id": "{{video.video_id}}",
        "destination_platform": "{{destino.platform}}",
        "destination_account_id": "{{destino.account_id}}",
        "result": "success", // ou "error"
        "platform_post_id": "{{post_id}}"
      }
   f. Google Sheets (Update) → Atualizar vídeo para "published"
   g. Google Sheets (Append) → Adicionar ao histórico
```

**Trigger:** Cron (a cada hora)

---

## 🎯 Exemplo Prático: Workflow 1 (Buscar Vídeos)

### Configuração dos Nodes:

**1. Google Sheets (Read)**
- Spreadsheet: Seu Google Sheets
- Sheet: Fontes
- Range: A:E (ou deixar vazio para tudo)
- Filters: `status = active`

**2. Code (ou Set)**
```javascript
// Formatar para o formato da API
const sources = $input.all().map(item => ({
  platform: item.json.platform,
  external_id: item.json.external_id,
  group_name: item.json.group_name
}));

return [{
  json: {
    sources: sources
  }
}];
```

**3. HTTP Request**
- Method: POST
- URL: `http://seu-servidor:8002/v1/n8n/process-sources`
- Ou se estiver na mesma VPS: `http://content-orchestrator:8000/v1/n8n/process-sources`
- Headers: `Content-Type: application/json`
- Body: `{{$json}}` (JSON)

**4. Split**
- Field to Split Out: `videos` (array da resposta)

**5. Loop (ou Split em Loop)**
- Para cada vídeo:
  - Google Sheets (Read) → Verificar se `video_id` existe
  - IF → Se não existe
  - Google Sheets (Append) → Adicionar vídeo

---

## 🔗 URLs dos Endpoints

**Na mesma VPS (dentro do Docker):**
- `http://content-orchestrator:8000/v1/n8n/process-sources`

**De fora da VPS (localmente ou outra máquina):**
- `http://seu-ip-vps:8002/v1/n8n/process-sources`
- `https://orchestrator.postagensapp.shop/v1/n8n/process-sources`

---

## 📋 Checklist para Começar

1. ✅ Google Sheets criado com 4 abas
2. ✅ Conectar Google Sheets no n8n (credenciais)
3. ✅ Criar Workflow 1 (Buscar vídeos)
4. ✅ Testar Workflow 1 manualmente
5. ✅ Criar Workflow 2 (Download)
6. ✅ Criar Workflow 3 (Publicar)
7. ✅ Configurar Cron triggers

---

## 🎬 Comece pelo Workflow 1!

Este é o mais simples e você verá resultados imediatos:
1. Busca vídeos das fontes
2. Adiciona no Google Sheets
3. Você pode ver os vídeos encontrados

Depois que funcionar, continue com os outros workflows.

---

**Dica:** Use o modo "Manual" primeiro para testar, depois configure os Cron triggers para automatizar!

