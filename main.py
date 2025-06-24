import discord
import logging
import os
from dotenv import load_dotenv, find_dotenv

from utils.configure_logger import ConfigureLogger
import bot

# retrieve discord's logger and configure logger
logger = logging.getLogger('discord')
discord_logger_config = ConfigureLogger(logger=logger)

# load environment variables from credentials.env
load_dotenv(override=True)
logger.info(f'Loading .env from {find_dotenv()}')

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = bot.Client(intents=intents)
    token = os.getenv('CLIENT_TOKEN')
    client.run(
        token=token
        , log_handler=None
    )

if __name__ == "__main__":
    main()