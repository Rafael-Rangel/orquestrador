#!/bin/bash
# Script de diagnóstico para VPS - comparar com ambiente local

echo "=========================================="
echo "DIAGNOSTICO: Ambiente VPS vs Local"
echo "=========================================="
echo ""

echo "1. Versao do Python:"
python3 --version
echo ""

echo "2. Versao do yt-dlp:"
yt-dlp --version
echo ""

echo "3. Versao do ffmpeg:"
ffmpeg -version | head -1
echo ""

echo "4. Teste de conectividade com YouTube:"
curl -I https://www.youtube.com 2>&1 | head -3
echo ""

echo "5. IP externo da VPS:"
curl -s ifconfig.me
echo ""
echo ""

echo "6. Teste simples do yt-dlp (sem cookies):"
yt-dlp --version --verbose 2>&1 | grep -i "version\|python\|extractor" | head -5
echo ""

echo "7. Verificar se cookies.txt existe e tamanho:"
if [ -f /app/data/cookies.txt ]; then
    echo "Arquivo existe: SIM"
    echo "Tamanho: $(wc -c < /app/data/cookies.txt) bytes"
    echo "Linhas: $(wc -l < /app/data/cookies.txt)"
else
    echo "Arquivo existe: NAO"
fi
echo ""

echo "8. Teste de download SEM cookies (cliente android):"
echo "Testando com: yt-dlp --extractor-args 'youtube:player_client=android' 'https://www.youtube.com/watch?v=jNQXAC9IVRw' --skip-download"
yt-dlp --extractor-args "youtube:player_client=android" "https://www.youtube.com/watch?v=jNQXAC9IVRw" --skip-download 2>&1 | tail -5
echo ""

echo "=========================================="
echo "FIM DO DIAGNOSTICO"
echo "=========================================="

