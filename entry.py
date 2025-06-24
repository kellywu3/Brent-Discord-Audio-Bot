import discord
from enum import Enum

from utils.timed_audio import TimedAudio

class Entry():
    def __init__(self, audio_metadata:tuple, message_information:tuple, timed_audio:TimedAudio):
        self.timed_audio = timed_audio
        self.audio_metadata = audio_metadata
        self.message_information = message_information

AUDIO_METADATA = ('title', 'url', 'duration')
class AudioMetadata(Enum):
    TITLE = 0
    URL = 1
    DURATION = 2

    # takes in the a dictionary from yt-dlp
    # returns a standardized audio metadata formated into a dict
    def retrieve_audio_metadata(audio:dict=None) -> tuple:
        if not audio:
            return None
        
        return tuple(audio[metadata] for metadata in AUDIO_METADATA)

MESSAGE_INFORMATION = ('author', 'channel', 'content')
class MessageInformation(Enum):
    AUTHOR = 0
    CHANNEL = 1
    CONTENT = 2

    # takes in the a message from discord
    # returns a standardized message information formated into a tuple
    def retrieve_message_information(message:discord.message=None) -> tuple:
        if not message:
            return None
        
        return tuple(getattr(message, information) for information in MESSAGE_INFORMATION)
