import os
import json

from utils import is_admin

@is_admin()
async def execute(message, args):
    # check if a argument was passed
    if len(args) == 0:
        await message.channel.send('Please specify a channel ID.')
        return
    
    # If argument was passed, check if it is a valid channel ID, if not, ask the user to try again
    try:
        channel_id = int(args[0])
    except ValueError:
        await message.channel.send('Please specify a valid channel ID.')
        return

    # If the channel ID is valid, check if the channel exists
    channel = message.guild.get_channel(channel_id)
    if channel is None:
        await message.channel.send('Please specify a valid channel ID.')
        return
    
    # if the channel exists and is valid Store the channel ID to a JSON file in the same directory as main.py
    # then send a message to the channel informing the user that the channel has been set for signals
    directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(directory, '..', 'channel.json')
    with open(filepath, 'w') as f:
        json.dump({'channel_id': channel_id}, f)

    # send a message to the channel specified by the user
    await channel.send('This channel has been set for signals.')
    await message.channel.send('Channel set for signals.')
