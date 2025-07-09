[back to README](../README.md)
# CONCEPTS
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