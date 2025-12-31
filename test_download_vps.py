#!/usr/bin/env python3
"""
Script de teste para download na VPS
Execute: python3 test_download_vps.py
"""
import sys
import os
import asyncio

# Adicionar app ao path
sys.path.insert(0, '/app')

from app.services.downloader.service import DownloaderService

async def test():
    print("=" * 60)
    print("Teste de Download com pytube/yt-dlp")
    print("=" * 60)
    print()
    
    service = DownloaderService()
    
    result = await service.download_video(
        video_url='https://www.youtube.com/shorts/qlIKbXlFkiE',
        platform='youtube',
        external_video_id='qlIKbXlFkiE',
        group_name='teste',
        source_name='@ShortsPodcuts'
    )
    
    print()
    print("=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'completed':
        print(f"✅ Arquivo salvo em: {result.get('path')}")
        if os.path.exists(result.get('path')):
            size = os.path.getsize(result.get('path'))
            print(f"   Tamanho: {size:,} bytes ({size/1024/1024:.2f} MB)")
    else:
        print(f"❌ Erro: {result.get('error')}")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    result = asyncio.run(test())
    sys.exit(0 if result.get('status') == 'completed' else 1)

