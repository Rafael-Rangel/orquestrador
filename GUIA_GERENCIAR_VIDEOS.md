# 📁 Guia: Como Gerenciar Vídeos Baixados

## 🔗 Como Funcionam os Volumes Docker

Os volumes Docker **compartilham o mesmo espaço físico**. Quando você:
- ✅ **Adiciona** um arquivo em qualquer lugar → aparece em todos
- ✅ **Remove** um arquivo de qualquer lugar → some de todos
- ✅ **Modifica** um arquivo em qualquer lugar → muda em todos

**São 3 caminhos diferentes para o MESMO lugar físico:**

1. **No container content-orchestrator**: `/app/downloads/`
2. **No container n8n**: `/content-downloads/`
3. **No host (VPS)**: `~/content-orchestrator/downloads/`

## 📍 Onde é Correto Mexer?

### ✅ **RECOMENDADO: No Host (VPS)**

```bash
# Listar vídeos
ls -lh ~/content-orchestrator/downloads/podcasts/@shortspodcuts/

# Mover vídeo
mv ~/content-orchestrator/downloads/podcasts/@shortspodcuts/video.mp4 ~/backups/

# Remover vídeo
rm ~/content-orchestrator/downloads/podcasts/@shortspodcuts/video.mp4

# Remover pasta inteira
rm -rf ~/content-orchestrator/downloads/podcasts/
```

### ✅ **Alternativa: Via Container (n8n)**

No n8n, você pode usar o nó "Execute Command":

```bash
# Listar
ls -lh /content-downloads/podcasts/@shortspodcuts/

# Remover
rm /content-downloads/podcasts/@shortspodcuts/video.mp4
```

### ⚠️ **Não Recomendado: Dentro do Container content-orchestrator**

Evite mexer diretamente dentro do container, a menos que seja necessário.

## 🗂️ Estrutura de Pastas

```
~/content-orchestrator/downloads/
├── podcasts/                    # group_name (minúsculas, espaços viram _)
│   ├── @shortspodcuts/          # source_name (minúsculas, espaços viram _)
│   │   ├── GRINGOS x PALAVRÕES....mp4
│   │   └── OUTRO VIDEO.mp4
│   └── outro_canal/
│       └── video.mp4
└── youtube/                     # Se não enviar group_name, usa platform
    └── video.mp4
```

## 📋 Comandos Úteis

### Listar todos os vídeos baixados:

```bash
# No host (VPS)
find ~/content-orchestrator/downloads -name "*.mp4" -type f

# Com tamanho
find ~/content-orchestrator/downloads -name "*.mp4" -type f -exec ls -lh {} \;
```

### Verificar espaço usado:

```bash
du -sh ~/content-orchestrator/downloads/*
```

### Limpar vídeos antigos (exemplo: mais de 30 dias):

```bash
find ~/content-orchestrator/downloads -name "*.mp4" -type f -mtime +30 -delete
```

### Mover vídeos para backup:

```bash
# Criar pasta de backup
mkdir -p ~/backups/videos

# Mover todos os vídeos
mv ~/content-orchestrator/downloads/podcasts/@shortspodcuts/*.mp4 ~/backups/videos/
```

## 🔍 Verificar se é o Mesmo Lugar

Para ter certeza de que são o mesmo lugar, teste:

```bash
# 1. Criar arquivo no host
touch ~/content-orchestrator/downloads/teste.txt

# 2. Verificar no container n8n
docker exec n8n ls /content-downloads/teste.txt

# 3. Verificar no container content-orchestrator
docker exec content-orchestrator ls /app/downloads/teste.txt

# Se aparecer nos 3 lugares = são o mesmo lugar! ✅
```

## ⚠️ Importante

- **Sempre use o caminho do host** (`~/content-orchestrator/downloads/`) para operações pesadas
- **No n8n**, use `/content-downloads/` para comandos rápidos
- **Evite** mexer dentro do container content-orchestrator diretamente
- **Backup**: Sempre faça backup antes de remover muitos arquivos

## 📝 Exemplo Prático

Se você quer **listar vídeos do grupo "PodCasts"**:

```bash
# No host (VPS) - RECOMENDADO
ls -lh ~/content-orchestrator/downloads/podcasts/*/

# Ou no n8n
ls -lh /content-downloads/podcasts/*/
```

Ambos mostram os mesmos arquivos! 🎯

