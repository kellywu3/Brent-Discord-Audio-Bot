# BRENT: Discord audio Bot

## OVERVIEW
all commands compatible with and executed on an M1 MacOS and a zshell terminal

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

## FEATURES
- have the bot join/leave a Voice Channel
- search audio from an input url or query
- play/pause/resume audio
- play from an audio queue with add/remove/print functionality


### NOT YET IMPLEMENTED
- implementing rewind/fast forward functionality
- implementing/testing different queue systems and functions
- implementing/testing different playlist
- implementing/testing different music providers
- using a database to store playlists and queues so that the playlists are saved in case the bot goes offline
- hosting the bot locally or externally


## REQUIREMENTS
- n/a

## LIBRARIES / DEPENDENCIES
### [discord.py](https://discordpy.readthedocs.io/en/stable/index.html#)
- Python API wrapper for Discord
- allows for bot programming through class-based inheritance or through function decorators
- [class-based inheritance vs. function decorators](class-based_inheritance.md)

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
- [os and dotenv vs. other options](os_dotenv.md)

### [yt-dlp](https://github.com/yt-dlp/yt-dlp/tree/master)
- command-line program and Python library used to download audio and video
- [yt-dlp vs. other options](yt-dlp.md)

### [FFmpeg](https://www.ffmpeg.org)
- cross platform command line program used to record, convert, and stream audio or video
- converts a compressed/encoded audio file into a raw PCM byte stream
- [FFmpegPCMAudio vs. other options](FFmpegPCMAudio.md)

### [validators](https://validators.readthedocs.io/en/latest/index.html)
- python data validation library
- checks if strings are valid types of data

[Enum](https://docs.python.org/3/library/enum.html)
- library that allows for enumerations, or a set of symbolic names bound to constant values
- used to enumerate the data stored in a collection data structures
- [enums vs. class constants](enums.md)

## TOOLS
### [Discord Developer Portal](https://discord.com/developers/)
- portal allowing developers to manage Discord applications

### [Pip](https://pypi.org/project/pip/)
- package installer for Python, included with Python 3.4 and higher

### [venv](https://docs.python.org/3/library/venv.html)
- Python built-in standard library virtual environment
- isolates Python library dependencies
- [venv vs. other options](venv.md)


## CONCEPTS
### Python
#### inheritance
- inheritance:
    - allows child class definitions that inherit all the methods and properties from a parent class
    - promotes code reusability, organization, and structure
- super function:
    - makes child classs inherit method and properties from parent
    - `super()` with a function call invokes the corresponding parent function

#### coroutines
- `async` functions:
    - represents a coroutine, functions that can pause and resume
    - allows for non-blocking execution; functions can operate independently without waiting for another
- `await` keyword (used inside `async` functions):
    - pauses execution until coroutine completes
    - waits for awaitable object before execution
    - allows for tasks to run concurrently by relinquishing control to the event loop

#### packing/unpacking
- unpacking/packing:
    - packing refers to grouping multiple values into a single variable
    - unpacking refers to extracting values from a packed variable
        - extracting into single variables
        - unpacking operators:
            - `*` for lists, tuples, and (technically) sets
            - `**` for dicts

#### safe attribute access
- using `getattr()`
    - allows an attempt to access attribute by name and return a default value if attribute is missing, returns attribute or defined return value

- using `hasattr()`
    - allows a check for the attribute, returns a bool

- Easier to Ask for Forgiveness than Permission (EAFP) using `try... except`
    - allows an attempt to execute access and prevents application termination if error occurs

- using `if... else`
    - use a check to handle specific cases

#### error handling and cleanup
- `try... except`
    - used to catch and handle specific errors/exceptions that would normally cause code to break and exit 
    - code within the `try` block may not work, but the code within the `except` block allows error exceptions

- `try... finally`
    - used to guarantee clean up code runs in cases like closing files, releasing locks, etc.
    - code within the `try` block may not work, but the code within the `except` block always runs

#### classes, class-based functions, and decorators
- classes 
    - serve as a blueprint for objects; each class represents a new type of object that can be instantiated
    - contain attributes to maintain its state and methods to modify its state

- class-based functions (methods)
    - functions defined within a class and operate within instances of that class
    - used for object oriented programming
    - include:
        - dunder/magic methods: double underscore methods; built-in functions that a class may inherit
        - instance methods: conventionally recieves `self` as the first argument; instance attributes are not shared between objects; method bound to an instance of the class and can access and/or modify instance attributes without affecting other instances
        - class methods: defined with `@classmethod` decorator and conventionally recieves `cls` as the first argument; class attributes are shared between all objects; method shared across all instances of classes
        - static methods: defined with `@staticmethod` decorator; method shared across all instances of classes but do not have access to instance or class variables

- decorators
    - decorator: function that takes another function as an argument and returns a new function with enhanced functionality; consists of a function definition that takes in a function argument, and a wrapper function body
    - `@[decorator] def func` syntax is shorhand for decorator(func)
    - classes can have decorator functions

```py
def decorator(func):
    def wrapper():
        ...
        func()
        ...
    return wrapper

@decorator
def hello():
    ...
```

#### built-in data structures and functions
- list:
    - ordered
    - mutable
    - defined using square brackets, `[]` or `list()`

- tuples:
    - ordered
    - immutable
    - defined using parentheses,, `()` or `tuple()`
    - requires a comma after the element when it has only one element

- sets:
    - unordered, do not allow duplicate values
    - mutable
    - defined using curly braces, `{}` or `set()` (empty sets must be initialized with the constructor)

- dictionaries (dicts):
    - unordered key-value pairs
    - mutable, (immutable keys)
    - defined using curly braces, `{}` or `dict()`

- `lambda` functions:
    - anonymous, short functions that don't require a full function definition
    - defined with the syntax: `lambda arguments: expression`

- `locals()`
    - returns a dictionary representing the current local symbol table
    - modifying the locals dict doesn't change the value of the variables

- `globals()`
    - returns a dictionary representing the current global symbol table
    - modifying the globals dict doesn't change the value of the variables

### Command Line Interface (CLI), Shell, and Shell Scripting
#### CLI, terminal, shell, shell scripting language
- CLI:
    - text-based interface
    - used by shells to interact with the operating system with commands

- terminal:
    - interchangable with console
    - application that provides the command line interface

- shell:
    - software program that interprets and processes user commands and passes them to the operating system (OS) for execution
    - generally has its own scripting languages

- shell scripting language:
    - programming language used to command a shell
    - most common shell scripts include:
        - Bash: developed for UNIX, UNIX-like OS such as GNU/Linux; Z shell (Zsh) is an extension of Bash
        - PowerShell: developed for Microsoft Windows
        - Python, JavaScript, Ruby, etc.

#### Shell and Shell Configuration Files
- shell configuration files:
    - text files that contain commands and settings used by the operating system to customize a shell environment such as by setting environment variables or setting custom functions
    - generally execute upon login and logout
    - specific configuration files dependent on shell type

- shell sessions and types of shell sessions:
    - shell session: current state/environment in the shell/terminal
    - interactive shell: shells that take user commands
    - non-interactive shell: shells that execute without interaction
    - login shell: shells provided to a user upon login; sources some different files from a non-login shell
    - non-login shell: shell that is invoked without a user first logging in; sources some different files from a login shell

- subshell:
    - separate instance of command process or "child" of the main shell that inherits the environment variables from its parent
    - allows change isolation within the subshell (changes to variables, functions, etc. that do not affect the parent shell's environment) and background/parallel processing (execution of commands while the parent shell continues without waiting for the process to complete)

- Zsh configuration files:
    - `~/.zshenv`: 
        - loaded universally for all types of shell sessions
        - sourced at every shell initialization
        - the only configuration file that gets loaded for non-interactive and non-login scripts (i.e. cron jobs, tasks that run automatically at predifined times or intervals)
        - rarely used due to universal loading
    - `~/.zprofile`
        - loaded for any type of login shells
        - sourced at every login shell initialization
        - subshells started within a terminal window inherit settings but don't load `~/.zprofile` again
    - `~/.zshrc`:
        - loaded for interactive shell sessions, when a new terminal window is opened or a subshell is launched
        - sourced at interactive shell initailization
    - `~/.zlogin`:
        - loaded for interactive login shells
        - similar to `~/.zprofile`, but sourced after `~/.zshrc` after login
    - `~/.zlogout`:
        - loaded for interactive login shells
        - sourced at logout when the login shell exits

### Libraries, Frameworks, Packages, Application Programming Interfaces 
#### libraries
- libraries:
    - reusable code; classes, functions, etc. that are embedded in software
    - focused on specific functionalities
    - library functions typically called by users

#### frameworks
- frameworks:
    - set of code, tools, libraries, and API's that provide a foundation for building applications with a specific structure
    - focused on supporting development of entire applications
    - user defined functions typically called by frameworks

#### packages
- packages:
    - collection of librariøes, frameworks, tools, etc.

#### application programming interfaces (API's)
- API's:
    - interface specifying how software interacts with another application
    - can be used to define interaction with a set of tools, functions, libraries, URL's, applications, etc.

- client:
    - application or software that interacts with another system or service through an API
    - uses an API to make requests and recieve responses

### Computer Architecture
#### memory
- random access memory/primary storage (RAM)
    - also refered to as data stored "in memory" or "main memory", focuses on fast memory access for CPU processing (the CPU checks the L1, L2, then L3 caches before fetching RAM data)
    - serves as a temporary data storage for the CPU
    - has a fast access speed and smaller capacity
    - data is volatile, or lost when the power is turned off

- disk memory/secondary storage
    - serves as a permanent data storage 
    - has a slow access speed and a larger capacity
    - data is non-volatile, or retained when the power is turned off

### Software Principles/Practices and Deign Patterns
#### software principles/practices
- object oriented programming (OOP)
    - programming model that organizes software around objects rather than functions/logic; focuses on:
        - encapsulation: bundling data, methods, states, etc. into a single unit (object), hiding internal details and allowing controlled access
        - abstraction: presenting only essential details to users and hiding implementation details
        - inheritance: allowing objects (child classes) to inherit properties and behaviors from existing objects (parent classes)
        - polymorphism: allowing different class objects to have a common parent class
    - modularity allows for improved organization, maintainability, reusability, scalability, etc.

- class relationships
    - inheritance (is-a): 
        - relationship where a class inherits the properties and behaviors of an existing class
        - promotes code reuse
        - represents objects of a same category
    - association:
        - relationship where a class/instance is loosely connected to another class/instance
    - aggregation (weaker has-a):
        - relationship where a class contains other classes
        - aggregate classes may exist independently
    - composition (has-a):
        - relationship where a class is composed of other classes that are essential to the main classes functionality

#### design patterns
- design patterns
    - reusable solutions to common problems during software development

- observer pattern
    - design pattern where an object (observer) listens and reacts to changes in another object
    - multiple triggers/events should cause the audio_player to play (calling play or the song ends and the next song should be played) a buffer is used in case the user decides to play a different song that is not in the playlist. the buffer allows for the music_player to retrieve or set the next music to be played in one place. the problem with just calling play is that it calls unnecessary checking (if statement) logic everytime it is called. for example, if the playlist is autoplaying a song that has already been retrieved, the play function needs to consider if its playing from the playlist or playing from a user input, when the function's logic would be much simpler if it focused solely on playing music from one source. using an observer pattern allows for a player function to play music when the source is updated. it creates an automatic play response to when a music is placed into the buffer which also allows us to separate the logic of dequing from the play command.


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

### [ ] Add to/create playlist

### [ ] Set up a server or computer to continue running the bot process
- local hosting

- cloud services (AWS, etc.)

- micro computers (arduino, raspberry pi, etc.)

## PROCESS (ARCHIVED TODO'S)
### [X] Create virtual environment (venv)
- create virtual environment

```Zsh
$ python -m venv /path/to/new/virtual/environment
 ```

- activate virtual environment
    - navigate to the project directory
    - activate the virtual environment

```Zsh
$ source ./bin/activate
```

- list all installed packages and versions

```Zsh
$ pip list
```

- install required packages given a `requirements.txt` file

```Zsh
$ pip install -r requirements.txt
```

- list installed packages and generate a `requirements.txt` file for installation

```Zsh
$ pip freeze > requirements.txt
```

- deactivate virtual environment within virtual environment

```Zsh
$ deactivate
```

- delete virtual environment
```Zsh
$ rm -rf /path/to/new/virtual/environment
```

### [X] Install discord.py within virtual environment
- install `discord.py` library to interact with Discord's API

```Zsh
$ pip install -U discord.py
```

### [X] Create bot on Discord Developer Portal
- create and set up bot
    - in Discord Developer navigate to `Bot > Privileged Gateway Intents`
    - under `PRESENCE INTENT`, `SERVER MEMBERS INTENT`, and `MESSAGE CONTENT INTENT`, toggle all as on

### [X] Invite bot to Discord
- generate URL with permissions to invite bot to Discord server
    - in Discord Developer navigate to `OAuth2 > OAuth2URLGenerator`
    - under `SCOPES`, check bot
    - under `BOT PERMISSIONS`, under `TEXT PERMISSIONS` and `VOICE PERMISSIONS`, check all
    - under `GENERATED URL`, copy

- invite bot to Discord server
    - paste generated URL in browser
    - under `ADD TO SERVER`, toggle to desired server
    - click `Continue` then `Authorize`

### [X] Connect application client to Discord
- create `main` file
    - import `discord.py` library to interact with the API wrapper for Discord's API

- create `main` function
    - in the `main` function define gateway intents
        - allows bot to subscribe to specified events
        - prevents bot from listening to spam events
        - set intents to default
        - set message content intent to true

```py
intents = discord.Intents.default()
intents.message_content = True
```

- create client file
    - import `discord.py` library

- create client class
    - inherit from `discord.Client`
        - allows Python functions to interact with Discord API 

```py
class Client(discord.Client):
```

- write test connectivity function
    - in the client class overwrite `discord.Client` `on_ready` asynchronous callback function
        - wait for events and triggers function call in response to events

```py
async def on_ready(self):
    print(f'Logged on as {self.user}')
```

- connect scripts to bot
    - in Discord Developer navigate to `Bot > Build-A-Bot`
    - under `TOKEN`, click `Reset Token` then `Yes, do it!` then enter password and click `Submit`
    - under `TOKEN`, copy the generated token
    - in the main function set the gateway intents of the client to the predefined intents
    - launch bot using client script and token
        - acts as bot's authentification and authorization

```py
client = bot.Client(intents=intents)
client.run(token='[token]')
```

- test connecting client to Discord bot
    - run main function

```Zsh
$ python main.py
```

### [X] Set up logging (logging)
- import `logging` library to set up logging messages
```py
import logging
```

- create `configure_logger` file to deal with repetitive logger configuration setups

- create class `ConfigureLogger` to configure each logger
    - create directory `logs` if the directory doens't exist using `os`, without sending an error message if logs exists
    - set the log level
    - configure the log output to send logs to separate `.log` files
    - format the log messages

```py
os.makedirs('logs', exist_ok=True)
```

- get logger for each class and configure logger using `ConfigureLogger` for each class

### [X] Separate password tokens from Python files (dotenv, os)
- install `python-dotenv` library to set environment variables using python

```Zsh
$ pip install python-dotenv
```

- import necessary libraries
    - `os` to retrieve environment variables
    - import `dotenv` 

- create `credentials.env` file to store credentials
    - set the Discord token 

```env
CLIENT_TOKEN=[token]
```

- load environment variables using `load_dotenv`
    - set the `override` variable to `True` so that changes to the `CLIENT_TOKEN` variable are loaded

```py
load_dotenv(override=True)
```

- retrieve the token using `os`

```py
os.getenv('CLIENT_TOKEN')
```

- use the credentials to log in as the Discord bot client

### [X] Retrieve stream URL from input (yt-dlp, validators)
- install and configure `yt-dlp` library to web scrape and retrieve stream URL's
    - install `yt-dlp`
    - import the `yt_dlp` library
    - configure `yt-dlp` options with a logger instance for ytdl to output logging messages and avoid non-video downloads
    - create a `yt-dlp` instance with the created options

```Zsh
$ pip install -U "yt-dlp[default]"
```

```py
logger = logging.getLogger('ytdl')
ytdl_manager_logger_config = ConfigureLogger(logger=logger)
ytdl_options = {
                'format': 'bestaudio/best'
                , 'default_search': 'auto'
                , 'noplaylist': True
                , 'extract_flat': True
                , 'force_generic_extractor': False
                , 'logger': logger
                }
ytdl = yt_dlp.YoutubeDL(ytdl_options)
```

- install `validators` to verify if an input is a valid URL

```Zsh
pip install validators
```

- check if the input is a URL or a search query
    - import `validators`
    - use `validators.url()` to check if the input is a valid URL

- use the input to retrieve the stream url
    - use the `yt-dlp` instance to
        - from a URL, extract the video metadata with `extract_info([URL], download=False)`
        - from a search query, extract video metadata with `ytdl.extract_info(f'ytsearch{[num results]}:{[search query]}', download=False)['entries']`

### [X] Retrieve a voice client for a user's voice channel from Discord
- retrieve a voice client to stream audio to a user's voice channel
    - retrieve the user's guild and channel
    - check if the user is in a voice channel
    - check if a voice client exists for the guild
    - use `discord.utils.get(self.client.voice_clients, guild=[guild], channel=[channel])` to retrieve a voice client

### [X] Play audio from Discord voice channel using a stream source (PyNaCl, FFmpeg)
- install `PyNaCl` for encryption and decryption of audio data transmitted through Discord

```Zsh
$ pip install pynacl
```

- install and configure `FFmpeg` for use with `Discord.py`
    - in FFmpeg's website, navigate to `Download`
    - under `Get packages & executable files`, download `FFmpeg` executables based on the operating system
    - move `ffmpeg.exe` to a `bin` folder within the project directory
    - initialize necessary `FFmpeg` file paths
        - initialize the path to write stderr messages
        - initialize the executable file path for `Discord.py` to access
    - set `FFmpeg` options using `Discord.py`'s API

```py
ffmpeg_stderr_path = [ffmpeg logging path]
ffmpeg_path = [ffmpeg.exe path]
ffmpeg_options = {
                'executable': ffmpeg_path
                , 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug'
                }
```

- create `play` function that streams audio to the voice channel using a stream URL
    - define `play` function that takes a URL as input and excepts and prints exceptions
    - stream the audio to the voice channel
        - open the `FFmpeg` stderr path with write options
        - use `voice_client.play(discord.FFmpegPCMAudio(source=[stream url], stderr=ffmpeg_stderr_file, **ffmpeg_options))` to stream audio to the voice channel
        - close the `FFmpeg` stderr path

### [X] Pause, resume, skip
- create function that pauses the stream in the voice channel
    - define function that excepts and prints exceptions
    - ensure that the voice client exists and the voice client is paused/playing before using `voice_client.pause()`/`voice_client.resume()`
    - use `voice_client.stop()` to stop the voice client

### [X] Retrieve response from bot prompt
- create function that waits for and retrieves a prompted response
    - define function that excepts and excepts `asyncio.TimeoutError` when a timeout occurs if the user does not respond within a timeout
    - define a function that checks the conditions of the response
    - use ```client.wait_for('message', check=[check function], timeout=[timeout])``` to retrieve the response message that meets the check criteria


## BUG FIXES AND ERRORS
### [X] FFmpeg stream disconnecting
bug:
- error arises while streaming audio for a long enough duration

```Zsh
[tls @ 0x12fe30530] Error in the pull function.
[tls @ 0x12fe30530] IO error: Connection reset by peer
[tls @ 0x12fe30530] The specified session has been invalidated for some reason.
    Last message repeated 1 times
[in#0/matroska,webm @ 0x12fe2fac0] Error during demuxing: Input/output error
```

solution:
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

### [X] Force quit a script that isn't responding

- use the process status command to find all currently running processes
    - show processes for all users, the owner of the process, and the background or detached processes
    - pipe the output to find processes that contain python

### [X] YT-DLP

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

## RESOURCES
- https://docs.python.org/3/howto/logging.html#logging-basic-tutorial