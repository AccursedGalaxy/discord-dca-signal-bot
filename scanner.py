import ccxt
import logging
import sys
from config import coins, exchanges, near_percentage, output_file

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def fetch_price(exchange, coin):
    """Fetch the price for a coin from an exchange."""
    try:
        return exchange.fetch_ticker(coin)['last']
    except Exception as e:
        logger.error(f"Could not fetch price for {coin} from {exchange.name}: {e}")
        return None

def check_levels(coin, levels, price):
    """Check if the price is near a DCA or profit level and write to a file."""
    with open(output_file, 'a') as f:
        for level_type, level_values in levels.items():
            for level in level_values:
                if (1 - near_percentage) * level <= price <= (1 + near_percentage) * level:
                    f.write(f"{coin} Hit a {level_type} Level: {level}\n")

def main():
    logger.info("Fitzos Levels:")
    logger.info("condition for signal is a range of 3% above or below the level")

    # Create exchange objects
    exchange_objects = [getattr(ccxt, name)() for name in exchanges]

    # Iterate over the coins
    for coin, levels in coins.items():
        # Fetch the price from the exchanges
        price = None
        for exchange in exchange_objects:
            price = fetch_price(exchange, coin)
            if price is not None:
                break

        # If no price was found, skip this coin
        if price is None:
            continue

        # Check if the price is near a DCA or profit level
        check_levels(coin, levels, price)

if __name__ == "__main__":
    main()
