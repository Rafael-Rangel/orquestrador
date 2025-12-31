"""
Serviço de download - stateless
Recebe dados, faz download e salva organizado
Suporta múltiplos métodos: pytube (principal) e yt-dlp (fallback)
"""
import os
import logging
from typing import Optional
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class DownloaderService:
    def __init__(self):
        """Serviço stateless - não precisa de sessão de banco"""
        pass

    async def download_video(
        self,
        video_url: str,
        platform: str,
        external_video_id: str,
        group_name: Optional[str] = None,
        source_name: Optional[str] = None
    ):
        """
        Faz download de um vídeo
        Organiza por: downloads/{grupo}/{fonte}/{video_id}.mp4
        Tenta primeiro com pytube, depois yt-dlp como fallback
        """
        # Organizar estrutura de pastas
        if group_name and source_name:
            group_folder = group_name.replace(" ", "_").lower()
            source_folder = source_name.replace(" ", "_").lower()
            download_dir = os.path.join(settings.LOCAL_STORAGE_PATH, group_folder, source_folder)
        else:
            download_dir = os.path.join(settings.LOCAL_STORAGE_PATH, platform)
        
        os.makedirs(download_dir, exist_ok=True)
        output_path = os.path.join(download_dir, f"{external_video_id}.mp4")

        # Tentar primeiro com pytube (mais simples, funciona melhor na VPS)
        try:
            logger.info(f"Trying pytube for {external_video_id}")
            result = await self._download_with_pytube(video_url, output_path)
            if result["status"] == "completed":
                return result
            else:
                logger.warning(f"pytube failed, trying yt-dlp: {result.get('error')}")
        except Exception as e:
            logger.warning(f"pytube error, trying yt-dlp: {e}")

        # Fallback para yt-dlp
        try:
            logger.info(f"Trying yt-dlp for {external_video_id}")
            return await self._download_with_ytdlp(video_url, output_path, external_video_id)
        except Exception as e:
            logger.error(f"Both methods failed for {external_video_id}: {e}")
            return {"status": "failed", "error": f"pytube and yt-dlp failed: {str(e)}"}

    async def _download_with_pytube(self, video_url: str, output_path: str):
        """Download usando pytubefix (versão atualizada do pytube)"""
        try:
            from pytubefix import YouTube
            from pytubefix.streams import Stream
            
            # Criar objeto YouTube com headers customizados para evitar bloqueios
            yt = YouTube(
                video_url,
                use_oauth=False,
                allow_oauth_cache=True
            )
            
            # Pegar melhor stream (vídeo + áudio ou melhor qualidade)
            try:
                # Tentar pegar stream progressivo (vídeo + áudio juntos)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if not stream:
                    # Se não tiver progressivo, pegar melhor vídeo
                    stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc().first()
            except:
                # Fallback: pegar qualquer stream MP4
                stream = yt.streams.filter(file_extension='mp4').first()
            
            if not stream:
                return {"status": "failed", "error": "No MP4 stream available"}
            
            # Download
            stream.download(output_path=os.path.dirname(output_path), filename=os.path.basename(output_path))
            
            # Verificar se arquivo foi criado
            if os.path.exists(output_path):
                logger.info(f"Downloaded with pytubefix: {output_path}")
                return {"status": "completed", "path": output_path}
            else:
                # Pytubefix pode salvar com extensão diferente
                base_path = output_path.replace('.mp4', '')
                for ext in ['.mp4', '.webm', '.3gp']:
                    if os.path.exists(base_path + ext):
                        final_path = base_path + ext
                        logger.info(f"Downloaded with pytubefix: {final_path}")
                        return {"status": "completed", "path": final_path}
                
                return {"status": "failed", "error": "File not found after download"}
                
        except Exception as e:
            logger.error(f"pytubefix download failed: {e}")
            return {"status": "failed", "error": f"pytubefix error: {str(e)}"}

    async def _download_with_ytdlp(self, video_url: str, output_path: str, external_video_id: str):
        """Download usando yt-dlp (fallback)"""
        import yt_dlp
        
        cookies_path = os.path.join(os.path.dirname(__file__), '../../data/cookies.txt')
        cookies_path = os.path.abspath(cookies_path)
        has_cookies = os.path.exists(cookies_path)
        
        # Estratégia simplificada: tentar android primeiro (funciona melhor)
        player_clients = ['android', 'tv', 'web']
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_path.replace('.mp4', '.%(ext)s'),
            'quiet': False,
            'extractor_args': {
                'youtube': {
                    'player_client': player_clients,
                }
            },
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
        }
        
        if has_cookies:
            ydl_opts['cookiefile'] = cookies_path
            logger.info(f"Using cookies file: {cookies_path}")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            logger.info(f"Downloaded with yt-dlp: {output_path}")
            return {"status": "completed", "path": output_path}
        except Exception as e:
            logger.error(f"yt-dlp download failed: {e}")
            return {"status": "failed", "error": f"yt-dlp error: {str(e)}"}
