import ccxt
import logging
from setup import exchanges, coins, near_percentage
from utils import loading_message

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

@loading_message
async def execute(message, args):
    response = await generate_dca_response()
    await message.channel.send(response)

