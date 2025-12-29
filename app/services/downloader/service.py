import yt_dlp
import hashlib
import os
import logging
from uuid import UUID
from app.models.content_item import ContentItem
from app.core.config import get_settings
from sqlmodel.ext.asyncio.session import AsyncSession

settings = get_settings()
logger = logging.getLogger(__name__)

class DownloaderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def download_item(self, content_item_id: UUID):
        from app.models.source import Source
        from app.models.group import Group
        from sqlmodel import select
        
        content_item = await self.session.get(ContentItem, content_item_id)
        if not content_item:
            logger.error(f"Content item {content_item_id} not found")
            return

        # Buscar source e group para organizar por estrutura grupo/fonte
        source = await self.session.get(Source, content_item.source_id)
        group_name = "unknown"
        source_name = "unknown"
        
        if source:
            source_name = source.external_id
            if source.group_id:
                group = await self.session.get(Group, source.group_id)
                if group:
                    group_name = group.name
        
        # Organizar por: downloads/{grupo}/{fonte}/{video_id}.mp4
        group_folder = group_name.replace(" ", "_").lower()
        source_folder = source_name.replace(" ", "_").lower()
        download_dir = os.path.join(settings.LOCAL_STORAGE_PATH, group_folder, source_folder)
        
        url = self._construct_url(content_item)
        output_path = os.path.join(download_dir, f"{content_item.external_video_id}.mp4")
        
        # Ensure directory exists
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Calculate Hash
            file_hash = self._calculate_hash(output_path)
            
            # Update Content Item
            content_item.storage_path = output_path
            content_item.content_hash = file_hash
            content_item.status = "downloaded"
            
            self.session.add(content_item)
            await self.session.commit()
            logger.info(f"Downloaded content {content_item.id}")

        except Exception as e:
            logger.error(f"Download failed for {content_item.id}: {e}")
            # Optionally set status to error?
            # content_item.status = "error"
            # self.session.add(content_item)
            # await self.session.commit()
            raise e

    def _construct_url(self, item: ContentItem) -> str:
        # Simplified
        if item.platform == "youtube":
            return f"https://www.youtube.com/watch?v={item.external_video_id}"
        return ""

    def _calculate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
