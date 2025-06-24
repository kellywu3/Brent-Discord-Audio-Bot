[back to README](README.md)
# Enums vs. Class Constants:
- Enums
    - symbolic names represented as integers
    - allows for type safety; integers or other data types cannot pass as an enumerated data type
    - allows for code hinting; accessing data from a dict with a key and value instead of a tuple/list with an enumeration requires knowledge of the key names
    - provides an easier ways to iterate through all enumerations
    - allows for readable and standardizable code with additional beneficial functionalities
    - values are referenced from a source that assigns a name an integer representation rather than hard coded as an integer

- Class Constants
    - constant variable names assigned integers
    - lacks type safety; integers may pass as valid symbolic variables but may cause errors if unchecked
    - allows for readable and standardizable code

## EXTRA LIBRARIES / DEPENDENCIES / TOOLS
- n/a

## PROCESS
### enums
- import `enum` module

- create Enum class
    - create child class that inherits the Enum class
    - initialize symbolic variable names with their associated value

```py
from enum import Enum

class AudioMetadata(Enum):
    TITLE = 0
    URL = 1
    DURATION = 2
```

### class constants
- create symbolic names class
    - initialize symbolic variable names with their associated value

```py
class AudioMetadata():
    TITLE = 0
    URL = 1
    DURATION = 2
```