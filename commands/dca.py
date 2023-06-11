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
    for level_type, level_values in levels.items():
        for level in level_values:
            if (1 - near_percentage) * level <= price <= (1 + near_percentage) * level:
                return f"{coin} Hit a {level_type} Level: {level}"
    return None

async def generate_dca_response():
    """Generate the DCA response."""
    response = "DCA Levels:\n"
    logger.info("Generating DCA response")

    try:
        prices = fetch_prices(coins.keys())
        if prices is not None:
            for coin, levels in coins.items():
                price = prices.get(coin)
                if price is not None:
                    result = check_levels(coin, levels, price)
                    if result:
                        response += f"{result} - Current Price: {price}\n"
                else:
                    response += f"Could not fetch price for {coin}.\n"

        return response
    except Exception as e:
        logger.error(f"Could not generate DCA response: {e}")
        return None


@loading_message
async def execute(message, args):
    response = await generate_dca_response()
    await message.channel.send(response)

