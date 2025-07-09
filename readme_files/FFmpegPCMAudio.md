[back to README](../README.md)
# discord.FFMpegPCMAudio vs. Other Options:
- built-in `discord.FFMpegPCMAudio`:
    - `discord.FFMpegPCMAudio` runs and handles `FFmpeg` subprocess
    - converts and streams audio, handles audio formatting with defined accepted `FFmpeg` parameters
    - allows less control over `FFmpeg` with execution, stream management, debugging and capturing stderr output
    - handles piping and streaming without needing to load full audio into memory, pipes PCM bytes to discord without full RAM buffering

- `discord.PCMAudio` with manual `FFmpeg`, `asyncio`, and `io`:
    - manually runs `FFmpeg` as a subprocess and pipes raw audio output to `discord.PCMAudio`
    - must manually feed audio url into `FFmpeg` and converted audio bytes into `discord.PCMAudio`
    - allows more control/flexibility over `FFmpeg` with capturing logs and input/output handling but prone to incompatibility
    - unable to stream audio directly to `FFmpeg`, requires buffering audio into RAM memory before processing with `FFmpeg`

- `discord.FFMpegPCMAudio` with `FFmpeg` post-processing through `yt-dlp`:
    - `yt-dlp` runs and handles `FFmpeg` suboprocess after downloading the compressed/encoded audio file
    - `yt-dlp` postprocessing does not support conversion to `pcm_s16le` and audio must be converted again
    - must manually feed converted audio bytes into `discord.PCMAudio`
    - unable to stream audio directly to `FFmpeg`, requires downloading audio (and deleting after use) into disk memory before processing with `FFmpeg`


## EXTRA LIBRARIES / DEPENDENCIES / TOOLS
### [asyncio](https://docs.python.org/3/library/asyncio.html)
- library used to write concurrent code
- includes:
    - event loops: execution schedules of tasks/coroutines
    - coroutines: functions defined with `async def`
    - tasks: wrappers around coroutines that can be scheduled and managed
    - futures: results of asynchronous operations that may not be available
    - task groups: multitask management

### [io](https://docs.python.org/3/library/io.html)
- library used to deal with various types of I/O
- I/O categorized into three main types: text I/O, binary I/O, raw I/O and can include streams and file-like objects


## PROCESS
### discord.FFmpegPCMAudio
- install and configure `FFmpeg`
    - in FFmpeg's website, navigate to `Download`
    - under `Get packages & executable files`, download ffmpeg executables based on the operating system
    - move `ffmpeg.exe` to a `bin` folder within the project directory

- configure necessary file paths and options
    - configure the ffmpeg path
    - configure the stderr output path
    - configure the ffmpeg options

```py
ffmpeg_stderr_path = [path]
ffmpeg_path = [path]
ffmpeg_options = {
                'executable': ffmpeg_path
                , 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug'
                }
```

- stream music to voice client
    - open the stderr output file with write options
    - use `discord.FFmpegPCMAudio` to convert an input audio url and pipe the output to discord voice client with the opened stderr output file and ffmpeg options as input
    - close the stderr output file

```py
ffmpeg_stderr_file = open(ffmpeg_stderr_path, 'w')
try:
    self.voice_client.play(discord.FFmpegPCMAudio(source=[audio url], stderr=ffmpeg_stderr_file, **ffmpeg_options))
finally:
    ffmpeg_stderr_file.close()
```

### discord.PCMAudio with manual FFmpeg and asyncio
- install and configure `FFmpeg`, `asyncio`, and `io`
    - in FFmpeg's website, navigate to `Download`
    - under `Get packages & executable files`, download ffmpeg executables based on the operating system
    - move `ffmpeg.exe` to a `bin` folder within the project directory
    - import `asyncio` to create a subprocess to run `FFmpeg` and convert audio to formated bytes
    - import `io` to convert bytes to bytestream

- configure necessary file paths
    - configure the ffmpeg path
    - configure the stderr output path

```py
ffmpeg_stderr_path = [path]
ffmpeg_path = [path]
```

- create a subprocess that manually runs the `FFmpeg` executable file
    - create the command line argument
        - define the `FFmpeg` path and audio url as inputs to `asyncio.create_subprocess_exec`
        - set up the format as raw PCM 16-bit signed little endian format, audio sample rate as 48kHz sampling rate, and of audio channels as 2 (used/expected by Discord)
        - send the output and error mesages to `stdout` and `stderr` using `-`
    - capture the `stdout` and `stderr` outputs (synonymous to using `>` in command line)

```py
process = await asyncio.create_subprocess_exec(
    ffmpeg_path
    , '-i', audio_url
    , '-f', 's16le'
    , '-ar', '48000'
    , '-ac', '2'
    , '-loglevel', 'debug'
    , '-'
    , stdout=asyncio.subprocess.PIPE
    , stderr=asyncio.subprocess.PIPE
)
```

- close the subprocess and pipe the outputs to corresponding locations
    - use `communicate()` to write reamining (empty) input and write the `stdout` and `stderr` to variables 
        - communicate waits for the subprocess to exit which prevents deadlocks
    - convert the stdout bytes to a bytestream using `io`
    - use `discord.PCMAudio` to pipe the output to discord voice client
    - open the stderr output file with write binary options and write the stderr output to the output file

```py
stdout, stderr = await process.communicate()
stream = io.BytesIO(stdout)

self.voice_client.play(discord.PCMAudio(stream=stream))

with open(ffmpeg_stderr_path, 'wb') as ffmpeg_stderr_file:
    ffmpeg_stderr_file.write(stderr)
```

### discord.PCMAudio with FFmpeg post-processing through yt-dlp
- n/a