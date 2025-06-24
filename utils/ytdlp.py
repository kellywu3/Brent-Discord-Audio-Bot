import logging
import yt_dlp

from utils.configure_logger import ConfigureLogger
from entry import AudioMetadata

# retrieve class logger and configure logger
logger = logging.getLogger('ytdl')
ytdl_manager_logger_config = ConfigureLogger(logger=logger)

class Yt_Dlp(yt_dlp.YoutubeDL):
    def __init__(self):
        ytdl_options = {
                'format': 'bestaudio/best'
                , 'default_search': 'auto'
                , 'noplaylist': True
                , 'extract_flat': True
                , 'force_generic_extractor': False
                , 'logger': logger
                }
        
        super().__init__(ytdl_options)

    def get_info(self, content:str='') -> dict:
        logger.info(f'Retrieving {content}')

        entry = self.extract_info(content, download=False)

        logger.info(f'Retrieved, filtering info')

        queried_info = AudioMetadata.retrieve_audio_metadata(entry)

        return queried_info

    def search_content(self, content:str='', max_results:int=5) -> list[tuple]:
        logger.info(f'Searching and retrieving {content}')

        results = self.extract_info(f'ytsearch{max_results}:{content}', download=False)
        entries = results['entries']

        logger.info(f'Search query "{content}" retrieved, filtering info')

        queried_info = []
        for entry in entries:
            print(f'getting audio meta for an entry')
            queried_info.append(AudioMetadata.retrieve_audio_metadata(entry))

        return queried_info