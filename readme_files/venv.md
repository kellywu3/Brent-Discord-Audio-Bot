[back to README](../README.md)
# venv vs. Other Options:
- `venv`
    - recommended over other virtual environments (virtualenv, pipenv, pyenv, poetry, conda etc.) for python native environments as it is built-into `Python3`
    - integrated from `virtualenv`, contains a subset of `virtualenv`'s features
    - supports `Python3`
    - creates a sandbox environment in current directory, supporting easily switchable environments for one project
    - creates a new directory,`$PATH` variable prepended with `env/bin`, with the system wide Python interpreter symlinked (copied) in the new directory; Python/Pip prioritizes packages from the local environment first before searching system-wide for dependencies

- `virtualenv`
    - integrated into `venv`
    - supports `Python2` and `Python3`
    - follows the same directory convention as `venv`

- `pipenv`
    - combines `Pipfile`, `Pip`, and `virtualenv` into one virtual environment tool
    - creates the virtual environment in a common, centralized virtual environment directory, supporting easily switchable environments between different projects
    - uses the default directory `~/.local/share/virtualenvs/[project name]`

## EXTRA LIBRARIES / DEPENDENCIES / TOOLS
### [virtualenv](https://virtualenv.pypa.io/en/latest/)
- virtual environment management tool integrated under the `venv` module

### [pipenv](https://pipenv.pypa.io/en/latest/)
- virtual environment management tool that bridges Pip and Python


## PROCESS
### venv
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

### virtualenv
- install `virtualenv`

```Zsh
$ pip install virtualenv
```

- create virtual environment

```Zsh
$ virtualenv /path/to/new/virtual/environment
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

### pipenv
- install `pipenv`

```Zsh
$ pip install pipenv
```

- create/activate virtual environment
    - navigate to the project directory

```Zsh
$ pipenv shell
```

- list all installed packages and versions

```Zsh
$ pipenv graph
```

- install required packages given a `requirements.txt` file

```Zsh
$ pipenv install -r requirements.txt
```

- list installed packages and generate a `requirements.txt` file for installation 

```Zsh
$ pipenv lock -r > requirements.txt
```

- exit virtual environment within virtual environment

```Zsh
$ exit
```

- delete virtual environment
```Zsh
$ pipenv --rm
```