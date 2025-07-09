[back to README](../README.md)
# Class-based Inheritance vs. Function Decorators:
- class-based inheritance and function decorators
    - allow for the same defined functionality with different code structures
    - just as only one parent function may be overriden by one child function with class-based inheritance, only one function can be registered per event with function decorators

- class-based inheritance:
    - encourages class creation due to inheritance and overriding methods instead of adding functions to the framework
    - allows for easier creation of object oriented code with states that allows for easier reusability
    - better for bots with more features, scripts that are reused between multiple bots, bots with ongoing updates, etc.

- function decorators:
    - encourages function/logic based code due to registering functions as handlers/callbacks instead of controlling predefined methods
    - allows for easier creation of "one-off" scripts that focus on specific, unique tasks that are unlikely to be reused
    - better for simple bots that do not require state maintenance 


## EXTRA LIBRARIES / DEPENDENCIES / TOOLS
- n/a


## PROCESS
### function decorators
- bot functionality created using class inheritance and overriding event listener coroutines
```py
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('my token goes here')
```

### class-based inheritance
- bot functionality created using decorators that define event listener functions
- does not require the client class to be run

```py
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
```

