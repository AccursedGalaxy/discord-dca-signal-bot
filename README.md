# Discord DCA Signal Bot

This is a Discord bot designed to provide real-time updates on Dollar Cost Averaging (DCA) levels for various cryptocurrencies. It sends unique signals to a specified channel, ensuring you never miss important changes.

## Features

- Real-time DCA level updates for various cryptocurrencies
- Unique signals sent to a specified channel
- Restricted command access for better security
- Commands:
  - `!dca`: Display current DCA levels
  - `!setchannel <channel_id>`: Set a channel for alerts

## Setup

1. Clone this repository: `git clone https://github.com/yourusername/discord-dca-signal-bot.git`
2. Navigate to the project directory: `cd discord-dca-signal-bot`
3. Install the required packages: `pip install -r requirements.txt`
4. Create a `.env` file in the `config` directory with the following variables:
   - `DISCORD_TOKEN`: Your Discord API token for the bot
   - `CHANNEL_ID`: The ID of the channel where the bot will send alerts
   - `CMC_API_KEY`: Your CoinMarketCap API key for price data
5. Copy `setup.py.example` to `setup.py` and fill in your own data: `cp setup.py.example setup.py`
6. Run the bot: `python main.py`

## Contributing

We welcome contributions from the community. Please read our [contributing guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE.md).

