import yt_dlp
import logging
import os
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.source import Source
from app.models.content_item import ContentItem
from app.models.group import Group
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class FetcherService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_from_source(self, source: Source):
        logger.info(f"Fetching from source: {source.id} ({source.platform})")
        
        # This is a simplified example using yt-dlp to get metadata
        # In a real scenario, you might use specific APIs for Instagram, TikTok, etc.
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True, # Don't download, just get metadata
            'force_generic_extractor': False,
        }

        # Construct URL based on platform and external_id (e.g., channel ID)
        url = self._construct_url(source)
        if not url:
            logger.warning(f"Could not construct URL for source {source.id}")
            return

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:
                    entries = info['entries']
                else:
                    entries = [info]

                for entry in entries:
                    if not entry:
                        continue
                        
                    external_video_id = entry.get('id')
                    title = entry.get('title')
                    upload_date = entry.get('upload_date') # YYYYMMDD
                    
                    if not external_video_id:
                        continue

                    # Check if exists
                    existing = await self.session.exec(
                        select(ContentItem).where(
                            ContentItem.platform == source.platform,
                            ContentItem.external_video_id == external_video_id
                        )
                    )
                    if existing.first():
                        continue
                    
                    # Parse date
                    published_at = datetime.utcnow()
                    if upload_date:
                        try:
                            published_at = datetime.strptime(upload_date, "%Y%m%d")
                        except ValueError:
                            pass

                    # Create ContentItem
                    new_item = ContentItem(
                        platform=source.platform,
                        external_video_id=external_video_id,
                        source_id=source.id,
                        published_at=published_at,
                        status="discovered"
                    )
                    self.session.add(new_item)
                    
                await self.session.commit()
                
        except Exception as e:
            logger.error(f"Error fetching from source {source.id}: {e}")

    def _construct_url(self, source: Source) -> str:
        if source.platform == "youtube":
            return f"https://www.youtube.com/channel/{source.external_id}"
        # Add other platforms
        return ""
