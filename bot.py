import ccxt
import logging
import discord
import asyncio

from config.settings import DISCORD_TOKEN, CHANNEL_ID
from setup import exchanges, coins, near_percentage

import responses

logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def fetch_price(exchange, coin):
    """Fetch the price for a coin from an exchange."""
    try:
        return exchange.fetch_ticker(coin)['last']
    except Exception as e:
        logger.error(f"Could not fetch price for {coin} from {exchange.name}: {e}")
        return None

def check_levels(coin, levels, price):
    """Check if the price is near a DCA or profit level."""
    for level_type, level_values in levels.items():
        for level in level_values:
            if (1 - near_percentage) * level <= price <= (1 + near_percentage) * level:
                return f"{coin} Hit a {level_type} Level: {level}"
    return None

async def generate_dca_response():
    """Generate the DCA response."""
    exchange_objects = [getattr(ccxt, name)() for name in exchanges]
    response = "DCA Levels:\n"

    try:
        for coin, levels in coins.items():
            found_price = False
            for exchange in exchange_objects:
                price = fetch_price(exchange, coin)
                if price is not None:
                    found_price = True
                    result = check_levels(coin, levels, price)
                    if result:
                        response += f"{result} - Current Price: {price}\n"
            if not found_price:
                response += f"Could not fetch price for {coin} from any exchange.\n"

        return response
    except Exception as e:
        logger.error(f"Could not generate DCA response: {e}")
        return None

async def send_message(message, user_message, is_private):
    try:
        if user_message == "!dca":
            response = await generate_dca_response()
        else:
            response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
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
            command = user_message[1:].lower()
            if command == "help" or command == "dca":
                await send_message(message, user_message, False)
        else:
            await send_message(message, user_message, False)

    client.run(TOKEN)

