import os
import importlib
import logging
import discord
from config.settings import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

commands = {}

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        commands[filename[:-3]] = importlib.import_module(f'commands.{filename[:-3]}')

async def send_message(message, user_message):
    try:
        if user_message.startswith('!'):
            command = user_message[1:].lower()
            if command in commands:
                await commands[command].execute(message, [])
    except Exception as e:
        logging.error(e)

def run_discord_bot():
    TOKEN = DISCORD_TOKEN
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        # check if the message is from the bot itself
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username}: {user_message} ({channel})')

        if user_message.startswith('!'):
            await send_message(message, user_message)
        else:
            await send_message(message, user_message)

    client.run(TOKEN)

