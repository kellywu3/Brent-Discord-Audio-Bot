import discord
import logging

import utils.misc as misc
from utils.configure_logger import ConfigureLogger
from audio_player import AudioPlayer

# retrieve class logger and configure logger
logger = logging.getLogger(__name__)
bot_logger_config = ConfigureLogger(logger=logger)

# create child class of discord.py Client
class Client(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_players = {}

    def get_audio_player(self, guild:discord.Guild) -> AudioPlayer:
        logger.info(f'Retrieving audio player from {guild}')
        
        if guild in self.audio_players:
            logger.info(f'Audio player found')
            return self.audio_players[guild]
        
        else:
            logger.info(f'Audio player not found, initializing audio player')
            self.audio_players[guild] = AudioPlayer(self)
            return self.audio_players[guild]
        
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.user.id:
            audio_player = self.get_audio_player(member.guild)
            await audio_player.handle_voice_state_update(member, before, after)

    async def on_ready(self):
        logger.info(f'Logged on as {self.user}')

    async def on_message(self, message):
        logger.info(f'Message from {message.author}: {message.content}')

        if message.author == self.user:
            return
        
        audio_player = self.get_audio_player(message.guild)
        
        match misc.get_first_n_words(message.content, 1):
            case '\\hello':
                await message.channel.send(f'Hello.')

            case'\\join':
                await audio_player.join_voice_channel(message)

            case '\\leave':
                await audio_player.leave_voice_channel(message)

            case '\\play':
                await audio_player.play(message)

            case '\\pause':
                await audio_player.pause(message)

            case '\\resume':
                await audio_player.resume(message)

            case '\\skip':
                await audio_player.skip(message)

            case '\\nowplaying':
                await audio_player.now_playing(message)

            case '\\list':
                await audio_player.list(message)

            case '\\add':
                await audio_player.add(message)

            case '\\remove':
                await audio_player.remove(message)