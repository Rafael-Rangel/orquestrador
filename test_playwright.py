"""
Teste do Playwright para download de vídeo do YouTube
"""
import asyncio
import sys
import os

# Adicionar app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.downloader.service import DownloaderService
from app.core.logging import setup_logging

setup_logging()

async def test():
    print("=" * 60)
    print("Teste de Download com Playwright")
    print("=" * 60)
    print()
    
    service = DownloaderService()
    
    print("Iniciando download...")
    print("URL: https://www.youtube.com/shorts/qlIKbXlFkiE")
    print()
    
    result = await service.download_video(
        video_url="https://www.youtube.com/shorts/qlIKbXlFkiE",
        platform="youtube",
        external_video_id="qlIKbXlFkiE",
        group_name="teste",
        source_name="@ShortsPodcuts"
    )
    
    print()
    print("=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'completed':
        path = result.get('path')
        print(f"SUCCESS: Arquivo salvo em: {path}")
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"Tamanho: {size:,} bytes ({size/1024/1024:.2f} MB)")
            print("Download concluido com sucesso!")
    else:
        print(f"ERROR: {result.get('error')}")
        print("ERROR: Download falhou!")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    try:
        result = asyncio.run(test())
        sys.exit(0 if result.get('status') == 'completed' else 1)
    except KeyboardInterrupt:
        print("\nERROR: Teste interrompido pelo usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

