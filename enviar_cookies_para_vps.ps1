# Script PowerShell para enviar cookies.txt para a VPS
# Uso: .\enviar_cookies_para_vps.ps1

$cookiesFile = "cookies.txt"
$vpsHost = "srv1011759"
$vpsUser = "root"
$vpsPath = "/root/content-orchestrator/data/cookies.txt"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Enviando cookies.txt para VPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o arquivo existe
if (-not (Test-Path $cookiesFile)) {
    Write-Host "ERRO: Arquivo $cookiesFile nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "Arquivo local: $cookiesFile" -ForegroundColor Green
Write-Host "Destino VPS: $vpsUser@$vpsHost`:$vpsPath" -ForegroundColor Green
Write-Host ""

# Tentar enviar usando SCP
Write-Host "Enviando arquivo..." -ForegroundColor Yellow

try {
    scp $cookiesFile "${vpsUser}@${vpsHost}:${vpsPath}"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS: Arquivo enviado com sucesso!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Proximos passos na VPS:" -ForegroundColor Cyan
        Write-Host "  1. Verificar: ls -la /root/content-orchestrator/data/cookies.txt" -ForegroundColor White
        Write-Host "  2. Verificar no container: docker exec -it content-orchestrator ls -la /app/data/cookies.txt" -ForegroundColor White
        Write-Host "  3. Testar download:" -ForegroundColor White
        Write-Host "     docker exec -it content-orchestrator bash" -ForegroundColor Gray
        Write-Host "     cd /app/downloads/teste/@shortspodcuts/" -ForegroundColor Gray
        Write-Host "     yt-dlp 'https://www.youtube.com/shorts/qlIKbXlFkiE' --cookies /app/data/cookies.txt --extractor-args 'youtube:player_client=android' -o 'qlIKbXlFkiE.%(ext)s'" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "ERRO: Falha ao enviar arquivo" -ForegroundColor Red
        Write-Host ""
        Write-Host "Alternativa: Use WinSCP ou FileZilla para fazer upload manualmente" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "ERRO: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternativa: Use WinSCP ou FileZilla para fazer upload manualmente" -ForegroundColor Yellow
    Write-Host "Ou copie o conteudo do arquivo cookies.txt e cole na VPS usando:" -ForegroundColor Yellow
    Write-Host "  nano /root/content-orchestrator/data/cookies.txt" -ForegroundColor Gray
}

