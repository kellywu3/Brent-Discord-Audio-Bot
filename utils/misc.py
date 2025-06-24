import validators

# checks if the input is a valid url
def validate_url(content:str='') -> bool:
    return validators.url(content) is True

# gets the first n words of a string
def get_first_n_words(content:str='', n:int=1) -> str:
    return ' '.join(content.split()[0:n])

# gets the remaining words after the first n words
def get_words_after_n(content:str='', n:int=0) -> str:
    return ' '.join(content.split()[n:])