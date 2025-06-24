import discord
import logging
import asyncio

import utils.misc as misc
from utils.ytdlp import Yt_Dlp
from utils.timed_audio import TimedAudio
from utils.configure_logger import ConfigureLogger
from entry import Entry, AudioMetadata, MessageInformation
from audio_queue import AudioQueueLinkedList

# retrieve class logger and configure logger
logger = logging.getLogger(__name__)
audio_player = ConfigureLogger(logger=logger)

# Discord API guidelines: one voice client is allowed per guild
# one audio player instance per guild
class AudioPlayer():
    MAX_RESULTS = 5

    def __init__(self, client:discord.Client):
        self.client = client
        self.voice_client = None
        self.yt_dlp = Yt_Dlp()
        self.audio_queue = AudioQueueLinkedList()
        self.entry_buffer = None

    async def retrieve_audio_metadata(self, message:discord.message) -> tuple:
        audio_metadata = None
        content = misc.get_words_after_n(message.content, 1)

        if content == '':
            await message.channel.send(f'Enter a song to the command.')
            return None
        
        # check if the content is a url and retrieve content accordingly
        if misc.validate_url(content):
            logger.info(f'Validated "{content}" as a url')

            audio_metadata = self.yt_dlp.get_info(content)

        else:
            logger.info(f'Invalidated "{content}" as a url')

            await message.channel.send(f'Searching for "{content}"')
            audio_metadatas = self.yt_dlp.search_content(content, self.MAX_RESULTS)

            printable = f'Choose a result:\n'
            for cnt in range(1, len(audio_metadatas) + 1):
                printable += f'{cnt}. {audio_metadatas[cnt - 1][AudioMetadata.TITLE.value]}\n'

            await message.channel.send(f'{printable}')
            
            try:
                msg = await self.client.wait_for('message', check=lambda m: m.author == message.author and m.channel == message.channel, timeout=30)
                msg_content = msg.content
                if msg_content.isdigit() and int(msg_content) > 0 and int(msg_content) <= self.MAX_RESULTS:
                    audio_metadata = audio_metadatas[int(msg_content) - 1]
                
                else:
                    await message.channel.send(f'Invalid input.')
                    return
            
            except asyncio.TimeoutError:
                logger.info(f'Response timed out, returning first entry')
                audio_metadata = audio_metadatas[0]
                await message.channel.send(f'Respond faster.')

        logger.info(f'Audio metadata retrieved: {audio_metadata}')
        return audio_metadata
    
    async def load_entry_buffer(self):        
        try:
            self.entry_buffer = self.audio_queue.dequeue()

            if self.entry_buffer:
                logger.info(f'Dequeued entry with {self.entry_buffer.audio_metadata} and {self.entry_buffer.message_information} from queue')
                await self.play_entry_buffer()

            else:
                logger.info(f'No more entries to dequeue')

        except Exception as e:
            logger.error(f'Error in load_entry_buffer function: {e}')

    async def play_entry_buffer(self, start_time:float=0):
        try:
            title = self.entry_buffer.audio_metadata[AudioMetadata.TITLE.value]
            # duration = self.entry_buffer.audio_metadata[AudioMetadata.DURATION.value]
    
            author = self.entry_buffer.message_information[MessageInformation.AUTHOR.value]
            channel = self.entry_buffer.message_information[MessageInformation.CHANNEL.value]
            logger.info(f'Playing {title} requested by {author} in channel {channel}')
            #  with duration {duration},

            def load_entry_buffer_sync(error:Exception=None):
                if error:
                    logger.error(f'Error in previous play_entry_buffer function: {error}')

                if not self.voice_client:
                    return

                coro = self.load_entry_buffer()
                fut = asyncio.run_coroutine_threadsafe(coro, self.client.loop)
                
                try:
                    fut.result()

                except Exception as e:
                    logger.error(f'Error in load_entry_buffer_sync function: {e}')

            await channel.send(f'Playing {title}.')
            source = self.entry_buffer.timed_audio
            self.voice_client.play(source=source, after=load_entry_buffer_sync)

        except Exception as e:
            logger.error(f'Error in play_entry_buffer function: {e}')

    def get_entry_buffer_printable(self) -> str:
        title = self.entry_buffer.audio_metadata[AudioMetadata.TITLE.value]
        duration = self.entry_buffer.audio_metadata[AudioMetadata.DURATION.value]
        elapsed_time = self.entry_buffer.timed_audio.get_elapsed_time()

        printable = f'Now playing: {title} [{elapsed_time}/{duration}]'
        return printable
    
    # sends the bot to the voice channel
    async def join_voice_channel(self, message:discord.message):
        try:
            # safe attribute access
            guild = message.author.guild
            channel = getattr(message.author.voice, 'channel', None)

            # check if the user is in a voice channel
            if not channel:
                logger.info(f'User not in voice channel')

                await message.channel.send(f'Join a voice channel.')
                return None

            voice_client = discord.utils.get(self.client.voice_clients, guild=guild, channel=channel)

            # check if a voice client exists
            if not voice_client:
                logger.info(f'Joining voice channel {channel}')
                voice_client = await channel.connect()

            else:
                logger.info(f'Already connected to a voice channel {channel}')

            self.voice_client = voice_client

        except Exception as e:
            logger.error(f'Error in join voice channel function: {e}')

    # removes the bot from the voice channel
    async def leave_voice_channel(self, message:discord.message):
        try:
            # check if the voice client is connected to a channel
            if self.voice_client:
                voice_client = self.voice_client
                self.voice_client = None

                logger.info(f'Disconnecting from voice channel {voice_client.channel}')
                await voice_client.disconnect()

            else:
                logger.info(f'Voice client not connected to any voice channel')

        except Exception as e:
            logger.error(f'Error in leave voice channel function: {e}')

    # sends the audio stream to the audio buffer to be played
    async def play(self, message:discord.message):
        await self.join_voice_channel(message)

        try:
            if self.voice_client:
                if not misc.get_words_after_n(message.content, 1) and not self.audio_queue.is_empty() and self.voice_client and not self.voice_client.is_playing():
                    logger.info("Calling load_entry_buffer from play function")
                    await self.load_entry_buffer()
                    return

                audio_metadata = await self.retrieve_audio_metadata(message)
                message_information = MessageInformation.retrieve_message_information(message)
                timed_audio = TimedAudio(audio_metadata[AudioMetadata.URL.value], 0)

                if audio_metadata and message_information:
                    self.entry_buffer = Entry(audio_metadata, message_information, timed_audio)
                    logger.info("Calling play_entry_buffer from play function")
                    await self.play_entry_buffer()

        except Exception as e:
            logger.error(f'Error in play function: {e}')

    # pauses the audio stream
    async def pause(self, message:discord.message):
        try:
            # check if the voice client is connected to a voice channel
            if not self.voice_client:
                logger.info(f'Voice client not connected to any voice channel')
                return
            
            # check if the voice client is streaming
            if not self.voice_client.is_playing():
                logger.info(f'Voice client not playing')
                return
                
            logger.info(f'Voice client paused')
            await message.channel.send(f'Paused.')
            self.voice_client.pause()

        except Exception as e:
            logger.error(f'Error in pause function: {e}')

    # resumes the audio stream
    async def resume(self, message:discord.message):
        try:
            # check if the voice client is connected to a voice channel
            if not self.voice_client:
                logger.info(f'Voice client not connected to any voice channel')
                return
            
            # check if the voice client is paused
            if not self.voice_client.is_paused():
                logger.info(f'Voice client not paused')
                return
            
            logger.info(f'Voice client resumed')
            await message.channel.send(f'Resumed.')
            self.voice_client.resume()

        except Exception as e:
            logger.error(f'Error in resume function: {e}')

    async def skip(self, message:discord.message):
        try:
            # check if the voice client is connected to a voice channel
            if not self.voice_client:
                logger.info(f'Voice client not connected to any voice channel')
                return
            
            # check if the voice client is playing
            if not self.voice_client.is_playing():
                logger.info(f'Voice client not playing')
                return

            logger.info(f'Voice client stopped to skip audio')
            await message.channel.send(f'Skipped.')
            self.voice_client.stop()

        except Exception as e:
            logger.error(f'Error in skip function: {e}')

    async def now_playing(self, message:discord.message):
        try:
            printable = self.get_entry_buffer_printable()
            if not printable:
                await message.channel.send(f'No audio playing.')

            else:
                await message.channel.send(f'Now playing:\n{printable}')

        except Exception as e:
            logger.error(f'Error in now_playing function: {e}')

    async def list(self, message:discord.message):
        try:
            printable = self.audio_queue.get_printable()
            if not printable:
                await message.channel.send(f'Queue is empty.')

            else:
                await message.channel.send(f'Current queue:\n{printable}')
        
        except Exception as e:
            logger.error(f'Error in list function: {e}')

    async def add(self, message:discord.message):
        try:  
            audio_metadata = await self.retrieve_audio_metadata(message)
            message_information = MessageInformation.retrieve_message_information(message)
            timed_audio = TimedAudio(audio_metadata[AudioMetadata.URL.value], 0)

            if audio_metadata and message_information and timed_audio:
                self.audio_queue.enqueue(audio_metadata, message_information, timed_audio)
                await message.channel.send(f'Enqueued {audio_metadata[AudioMetadata.TITLE.value]}.')
                logger.info(f'Added entry with {audio_metadata} and {message_information} to queue')
            
        except Exception as e:
            logger.error(f'Error in add function: {e}')

    async def remove(self, message:discord.message):
        try:  
            content = misc.get_words_after_n(message.content, 1)
            entry = None
            if content.isdigit():
                entry = self.audio_queue.remove(int(content))

            if entry:
                await message.channel.send(f'Removed {entry.audio_metadata[AudioMetadata.TITLE.value]}.')
                logger.info(f'Removed entry with {entry.audio_metadata} and {entry.message_information} from queue')

            else:
                await message.channel.send(f'Invalid input.')
                return
            
        except Exception as e:
            logger.error(f'Error in add function: {e}')