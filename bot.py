import os
import importlib
import logging
import discord
from discord.utils import find
from discord.ext import commands, tasks
import json
from config.settings import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

command_modules = {}


command_modules['setchannel'] = importlib.import_module('commands.setchannel')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        command_modules[filename[:-3]] = importlib.import_module(f'commands.{filename[:-3]}')

async def send_message(message, user_message):
    try:
        if user_message.startswith('!'):
            command = user_message[1:].lower()
            if command in command_modules:
                await command_modules[command].execute(message, [])
    except Exception as e:
        logging.error(e)


@tasks.loop(minutes=5) # one minute for testing
async def check_dca_levels(client):
    response = await command_modules['dca'].generate_dca_response()

    # try to read the old response, handle the case where the file doesn't exist or is empty
    try:
        with open('dca_response.json', 'r') as f:
            old_response = f.read()
    except (FileNotFoundError, IOError):
        old_response = ""
        logging.info("No previous response found.")

    # write the new response to the file
    with open('dca_response.json', 'w') as f:
        f.write(response)

    # send only unique lines of the response to the channel
    new_lines = [line for line in response.split('\n') if line and line not in old_response.split('\n')]
    if new_lines:
        logging.info(f"New lines found: {new_lines}")
        # get channel id from channel.json
        try:
            with open('channel.json', 'r') as f:
                channel_id = json.load(f)['channel_id']
        except (FileNotFoundError, IOError, KeyError):
            logging.error("Failed to get channel ID.")
            return
        channel = client.get_channel(int(channel_id))
        if channel is not None:
            embed = discord.Embed(title="New Levels:", description="\n".join(new_lines), color=0x00ff00)
            await channel.send(embed=embed)
    else:
        logging.info(f"No new lines found in response.")

    logging.info("Finished checking DCA levels.")




def run_discord_bot():
    TOKEN = DISCORD_TOKEN

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        check_dca_levels.start(client)

    @client.event
    async def on_guild_join(guild):
        print(f'{client.user} has joined {guild.name}!')
        channel = guild.system_channel
        if channel is None or not channel.permissions_for(guild.me).send_messages:
            # If the bot can't send messages in the system channel, find another one
            channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
        if channel is not None:
            await channel.send('Hello {}!'.format(guild.name))
            await channel.send('Please setup a channel for signals with !setchannel <channel_id>')

    @client.event
    async def on_message(message):
        # check if the message is from the bot itself
        if message.author == client.user:
            return

        logging.info(f"Message received: {message.content}")

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username}: {user_message} ({channel})')

        if user_message.startswith('!'):
            # split the user message into command and arguments
            command = user_message[1:].lower().split(' ')[0]
            args = user_message[1:].lower().split(' ')[1:]

            # Check if the command exists in the commands dictionary
            if command in command_modules:
                module = command_modules[command]
                await module.execute(message, args)
            else:
                await send_message(message, user_message)
        else:
            await send_message(message, user_message)

    client.run(TOKEN)

