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

    # returns a list of audio metadata tuples
    def retrieve(self, content:str='', max_results:int=1) -> list[tuple]:
        logger.info(f'Searching and retrieving {content}')

        results = self.extract_info(f'ytsearch{max_results}:{content}', download=False)
        entries = results['entries']

        logger.info(f'Search query "{content}" retrieved, filtering info')

        queried_info = []
        for initial_entry in entries:
            url = initial_entry['webpage_url']
            logger.info(f'extracting entry from {url}')

            entry = self.extract_info(url, download=False)
            entry_metadata = AudioMetadata.retrieve_audio_metadata(entry)
            logger.info(f'retrieved metadata:\n{entry_metadata}')
            
            queried_info.append(entry_metadata)

        return queried_info