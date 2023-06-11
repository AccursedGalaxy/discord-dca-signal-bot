import requests
import logging
from setup import coins, near_percentage
from utils import loading_message

from config.settings import CMC_API_KEY

logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)



def fetch_prices(coins):
    """Fetch the prices for multiple coins from CoinMarketCap."""
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }
    parameters = {
        "symbol": ','.join(coins),
        "convert": "USD"
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()['data']
        prices = {coin: float(data[coin]['quote']['USD']['price']) for coin in coins}
        logger.info(f"Prices: {prices}")
        return prices
    except Exception as e:
        logger.error(f"Could not fetch prices: {e}")
        return None


def check_levels(coin, levels, price):
    """Check if the price is near a DCA or profit level."""
    logger.info(f"Checking levels for {coin} at {price}")
    level_hits = {}
    for level_type, level_values in levels.items():
        for level in level_values:
            if (1 - near_percentage) * level <= price <= (1 + near_percentage) * level:
                level_hits[level_type] = level
    return level_hits if level_hits else None


async def generate_dca_response():
    """Generate the DCA response."""
    response = "Here is your Levels Update:\n\n"
    logger.info("Generating DCA response")

    # Initialize dictionaries to store coins that hit each level
    dca_hits = {}
    target_hits = {}
    bullrun_hits = {}

    try:
        prices = fetch_prices(coins.keys())
        if prices is not None:
            for coin, levels in coins.items():
                price = prices.get(coin)
                if price is not None:
                    result = check_levels(coin, levels, price)

                    # Check which level was hit and add to the appropriate dictionary
                    if result:
                        if 'DCA' in result:
                            dca_hits[coin] = result['DCA']
                        if 'Target' in result:
                            target_hits[coin] = result['Target']
                        if 'BullRunTarget' in result:
                            bullrun_hits[coin] = result['BullRunTarget']

                else:
                    response += f"Could not fetch price for {coin}.\n"

        # Add DCA hits to the response
        if dca_hits:
            response += "DCA Targets Hit On These Coins:\n"
            for coin, info in dca_hits.items():
                response += f"{coin} Hit a DCA Level: {info}\n"

        # Add Target hits to the response
        if target_hits:
            response += "\nProfit Target Hit On These Coins:\n"
            for coin, info in target_hits.items():
                response += f"{coin} Hit a Target Level: {info}\n"

        # Add BullRunTarget hits to the response
        if bullrun_hits:
            response += "\nBull Run Target Hit On These Coins:\n"
            for coin, info in bullrun_hits.items():
                response += f"{coin} Hit a Bull Run Target Level: {info}\n"

        return response
    except Exception as e:
        logger.error(f"Could not generate DCA response: {info}\n")
        return None


@loading_message
async def execute(message, user_message):
    response = await generate_dca_response()
    await message.channel.send(response)

