"""
Script de teste para download de vídeo localmente
"""
import asyncio
import sys
import os

# Adicionar o diretório app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.downloader.service import DownloaderService
from app.core.logging import setup_logging

setup_logging()

async def test_download():
    """Testa o download do vídeo"""
    downloader = DownloaderService()
    
    result = await downloader.download_video(
        video_url="https://www.youtube.com/shorts/qlIKbXlFkiE",
        platform="youtube",
        external_video_id="qlIKbXlFkiE",
        group_name="teste",
        source_name="@ShortsPodcuts"
    )
    
    print("\n" + "="*50)
    print("RESULTADO DO DOWNLOAD:")
    print("="*50)
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'completed':
        print(f"Arquivo salvo em: {result.get('path')}")
    else:
        print(f"Erro: {result.get('error')}")
    print("="*50 + "\n")
    
    return result

if __name__ == "__main__":
    print("Iniciando teste de download...")
    print("URL: https://www.youtube.com/shorts/qlIKbXlFkiE")
    print("Aguarde...\n")
    
    result = asyncio.run(test_download())
    
    if result.get('status') == 'completed':
        print("SUCCESS: Download concluido com sucesso!")
        sys.exit(0)
    else:
        print("ERROR: Download falhou!")
        sys.exit(1)

