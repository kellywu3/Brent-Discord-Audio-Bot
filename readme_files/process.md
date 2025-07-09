[back to README](../README.md)
# PROCESS (Archived Todo's)
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
$ rm -rf /path/to/virtual/environment
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