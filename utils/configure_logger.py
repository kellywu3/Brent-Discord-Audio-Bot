import logging
import os
import contextvars
from contextlib import contextmanager

# handles output to separate files and configures logger output
class ConfigureLogger():
    # make logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # initialize
    def __init__(self, logger:logging.Logger, log_level:int=logging.DEBUG):
        # set logger as an instance variable
        self.logger = logger

        # set log level
        self.logger.setLevel(log_level)

        # set up logging handler to write logs to separate .log files in the logs directory
        self.filename = f'logs/{self.logger.name}.log'
        handler = logging.FileHandler(
            filename=self.filename
            , encoding='utf-8'
            , mode='w'
        )
        self.logger.addHandler(handler)

        # format log messages 
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {funcName}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)