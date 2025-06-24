import discord
import os

# configure stderr and ffmpeg path for discord.py
ffmpeg_stderr_path = os.path.join(os.getcwd(), 'logs', 'ffmpeg.log')
ffmpeg_path = os.path.join(os.getcwd(), 'bin', 'ffmpeg')

# create child class of discord.py Client
# one timed FFmpegPCMAudio instance per audio
class TimedAudio(discord.FFmpegPCMAudio):
    def __init__(self, source:str='', start_time:int=0):
        self.start_time = start_time
        self.elapsed_time = 0
        self.ffmpeg_stderr_file = open(ffmpeg_stderr_path, 'w')

        ffmpeg_options = {
                'executable': ffmpeg_path
                , 'stderr': self.ffmpeg_stderr_file
                , 'before_options': f'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug  -ss {self.start_time}'
                , 'options': '-vn'
                }

        super().__init__(source=source, **ffmpeg_options)

    def cleanup(self):
        self.ffmpeg_stderr_file.close()
        super().cleanup()

    def read(self) -> bytes:
        self.elapsed_time += 20
        return super().read()
    
    def get_elapsed_time(self):
        return self.elapsed_time / 1000 + self.start_time