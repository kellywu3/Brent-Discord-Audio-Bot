[back to README](../README.md)
# os and dotenv vs. Other Options:
- `os` and `dotenv`:
    - environment variables are set from a `.env` file, loaded using the `dotenv` library and retrieved using the `os` library
    - allows credentials to stay separate from code and environment variables to be loaded at runtime
    - variables loaded by `load_dotenv` do not persist after the python terminates
    - while the password isn't stored directly in code, loading the environment variables in code still poses security risks; encrypting the `.env` file or using a secrets manager can further help mitigate security issues

- `os`:
    - environment variables are inherited from parent and must be defined with each new shell or in the shell startup file `~/.zprofile` or `~/.zshenv` to be used across all new shells
    - defining environment variables in `~/.zprofile` causes all shell instances for a user to load the passwords as environment variables
    - defining environment variables in `~/.zshenv` (not recommended) causes all shell instances to load the passwords as environment variables
    - evironment variables do not provide encryption; encrypting the environment variables can further help mitigate security issues

- `cryptography` encryption:
    - token is encrypted using a generated encryption key, the encrypted token is stored and decrypted at runtime with the encryption key
    - requires a safe place to store the encryption key
    - unnecessary for tokens loaded from a personal environment variable
    - storing passwords in a `.py` file may have a higher chance of accidental password leaks to version control systems (VCS)


## EXTRA LIBRARIES / DEPENDENCIES / TOOLS
### [Vim](https://www.vim.org) 
- configurable text editor to write and edit text files; improved version of the original Vi text editor
- can be controlled entirely with the keyboard

### [cryptography](https://cryptography.io/en/latest/)
- library that includes high and low level cryptographic algorithms


## PROCESS
### os and dotenv
- install `python-dotenv` library
```Zsh
$ pip install python-dotenv
```

- import necessary libraries
    - `os` to retrieve environment variables
    - import `dotenv` to set environment variables using python

- create `credentials.env` file to store credentials
    - set the discord token 

```env
CLIENT_TOKEN=[token]
```

- load environment variables using `load_dotenv`

```py
load_dotenv()
```

- retrieve the token using `os`

```py
os.getenv('CLIENT_TOKEN')
```

- use the credentials to log in as the discord bot client

### os
- import `os` to retrieve environment variables

- set environment variables in `~/.zprofile`
    - use Vim to edit the `~/.zprofile` file
        - if the file does not exist, vim will open an empty buffer for that file
    - set the `CLIENT_TOKEN` environment variable
        - use `o` to open a new line and enter insert mode
        - enter the `export` command to set the `CLIENT_TOKEN` variable
        - use `Esc` to exit insert mode
        - use `:wq` and `Enter` to enter command-line mode, write/save the current file and quit the editor

```Zsh
$ vim ~/.zprofile
```

```Zsh
$ export CLIENT_TOKEN=[token]
```

- retrieve the token using `os`

```py
os.getenv('CLIENT_TOKEN')
```

### cryptography encryption
- n/a
