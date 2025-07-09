# BRENT: Discord audio Bot

## OVERVIEW
all commands compatible with and executed on an M1 MacOS and a zshell terminal

## FEATURES
- have the bot join/leave a Voice Channel
- search audio from an input url or query
- play, pause, resume, skip audio
- play from an audio queue (linked list) with add, remove, print functionality


### NOT YET IMPLEMENTED
- rewind/fast forward functionality
- implement/test different queue systems and functions
- implement/test different playlist
- implement/test different music providers
- using a database to store playlists and queues so that the playlists are saved in case the bot goes offline
- hosting the bot locally or externally


## REQUIREMENTS
- n/a

## LIBRARIES / DEPENDENCIES
### [discord.py](https://discordpy.readthedocs.io/en/stable/index.html#)
- Python API wrapper for Discord
- allows for bot programming through class-based inheritance or through function decorators
- [class-based inheritance vs. function decorators](./readme_files/class_based_inheritance.md)

### [PyNaCl](https://pypi.org/project/PyNaCl/)
- cryptography library used to improve message encoding/decoding usability, security, and speed
- required to access voice through as a discord.py client

### [logging](https://docs.python.org/3/library/logging.html)
- Python's built-in standard library logging system
- allows logging messages to integrate third party messages

### [asyncio](https://docs.python.org/3/library/asyncio.html)
- library used to write single threaded concurrent code

### [os](https://docs.python.org/3/library/os.html)
- module that provides miscellaneous operating system dependent functions such as retrieving environment variables, reading/writing files, making directories, etc.

### [dotenv](https://pypi.org/project/python-dotenv/)
- library that loads key value pairs from a `.env` file and sets the pairs up as environment variables
- [os and dotenv vs. other options](./readme_files/os_dotenv.md)

### [yt-dlp](https://github.com/yt-dlp/yt-dlp/tree/master)
- command-line program and Python library used to download audio and video
- [yt-dlp vs. other options](./readme_files/yt-dlp.md)

### [FFmpeg](https://www.ffmpeg.org)
- cross platform command line program used to record, convert, and stream audio or video
- converts a compressed/encoded audio file into a raw PCM byte stream
- [FFmpegPCMAudio vs. other options](./readme_files/FFmpegPCMAudio.md)

### [validators](https://validators.readthedocs.io/en/latest/index.html)
- python data validation library
- checks if strings are valid types of data

### [Enum](https://docs.python.org/3/library/enum.html)
- library that allows for enumerations, or a set of symbolic names bound to constant values
- used to enumerate the data stored in a collection data structures
- [enums vs. class constants](./readme_files/enums.md)

### [functools](https://docs.python.org/3/library/functools.html)
- module for higher order functions (functions that act on or return other functions)
- used to preserve function metadata when using function decorators

## TOOLS
### [Discord Developer Portal](https://discord.com/developers/)
- portal allowing developers to manage Discord applications

### [Pip](https://pypi.org/project/pip/)
- package installer for Python, included with Python 3.4 and higher

### [venv](https://docs.python.org/3/library/venv.html)
- Python built-in standard library virtual environment
- isolates Python library dependencies
- [venv vs. other options](./readme_files/venv.md)


## CONCEPTS
[notes on new concepts](./readme_files/concepts.md)


## TODO'S
### [-] Rewind/Fast forward
- should use `\rewind [amount of time in seconds]` to rewind 
- should use `\forward [amount of time in seconds]` to fast forward 

- create `timed_audio` object to keep track of the amount of time elapsed while reading/playing a `discord.FFmpegPCMAudio` source
    - create `timed_audio` script file
    - create class `TimedAudio` to maintain time states
        - inherit from `discord.FFmpegPCMAudio` to override and add functionality to existing `FFmpeg`

### [-] Create and test various queues
FIFO queue class
enqueue
dequeue
remove
print

can take in playlist and shuffle (shuffles a list of indices and feeds to queue)

### [-] Play music continuously from queue

### [-] Add to, remove from, and list queue commands

### [ ] Add to, remove from, create new, and delete playlist command

### [ ] Create playlist and playlist functionality
- writing to in memory data structure
    - inputting to a list

- writing to a file (json)
    - can be troublesome with multiple read/writes?
    - what happens when multiple users use the same bot?

- writing to Redis
    - NoSQL
    - writes to in memory RAM
    - expects computer to be running at all times

- writing to SQL server

- writing to local SQL server

- writing to mongoDB

### [-] Add to/create playlist

### [ ] Set up a server or computer to continue running the bot process
- local hosting

- cloud services (AWS, etc.)

- micro computers (arduino, raspberry pi, etc.)

## PROCESS
[archived todo's](./readme_files/process.md)


## BUG FIXES AND ERRORS
### [X] FFmpeg stream disconnecting
- error arises while streaming audio for a long enough duration

```Zsh
[tls @ 0x12fe30530] Error in the pull function.
[tls @ 0x12fe30530] IO error: Connection reset by peer
[tls @ 0x12fe30530] The specified session has been invalidated for some reason.
    Last message repeated 1 times
[in#0/matroska,webm @ 0x12fe2fac0] Error during demuxing: Input/output error
```

- issue addressed by others at yt-dlp: https://github.com/yt-dlp/yt-dlp/issues/8854
- add options to ffmpeg to automatically reconnect, allow reconnection to streamed sources, and set the maximum delay between reconnection attempts to five seconds

```py
ffmpeg_options = {
                'executable': ffmpeg_path
                , 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug'
                }

self.voice_client.play(discord.FFmpegPCMAudio(source=info['url'], stderr=ffmpeg_stderr_file, **ffmpeg_options))
```

### [X] Passing a coroutine to the player's after function
- issue addressed by discord.py: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-pass-a-coroutine-to-the-player-s-after-function
- create a callable that wraps a coroutine scheduled to run on the bot's event loop

```py
def [after function](error:Exception=None):
    if error:
        print(f'{error}')

    coro = self.load_entry_buffer()
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
    try:
        fut.result()

    except Exception as e:
        print(f'{e}')

self.voice_client.play(source=[source], after=[after function])
```

### [X] Force quitting a script that isn't responding

- use the process status command to find all currently running processes
    - show processes for all users, the owner of the process, and the background or detached processes
    - pipe the output to find processes that contain python

```zsh
ps aux | grep python
```

- identify the process running the script
    - the process has the format `[user] [PID] [%CPU] [%MEM] [VSZ] [RSS] [TTY] [STAT] python [python script]`
    - identify the process id (PID) running the python script name

- kill the process

```zsh
kill [PID]
```

### [X] Extracting full metadata using yt-dlp
- 

## RESOURCES
- https://docs.python.org/3/howto/logging.html#logging-basic-tutorial

### Design Questions
- how should the functions be organized into files and folders?
- to what extent should functions be modularized or abstracted?
- which function should process the metadata retrieved from `yt-dlp`?
- what are security risks with the client token and how can they be mitigated?
- what are all of the ways that each feature can be implemented and what are their pros and cons?
- how can the code implement a standard/constraint for exchanged metadata for reusability, readability, and error prevention?
    - classes that first recieve data should filter/format (if necessary) the data for the rest of the system
    - functions/classes should hide its internal logic and reveal only what is necessary to users (abstractions)
    - functions/classes that depend on other existing functions/classes should work around whats given instead of modifying what exists (unless it is necessary to modify a function/class to create better modularity)
- what various data structures for the queue can be tested for runtime speed and efficiency? how should the tests be set up?
- what could and should be implemented to speed up overall runtime?
- during runtime, are there any data leaks? how can we flush data that no longer has use? how does python's garbage collection work with the software?
- how can the bot store search results and wait for further input from search results?
- what can be used to host the bot indefinitely? what can be used to store data in case the bot goes offline?
- should the logger configuration class inherit from the existing logger library or compose extra functionality? when should a class inherit? (class relationships, functionality extension, polymorphisms)