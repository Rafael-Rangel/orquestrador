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


